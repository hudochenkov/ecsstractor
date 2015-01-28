import sublime
import sublime_plugin
import re
import os

try:
	# ST2, Python 2
	from HTMLParser import HTMLParser
except:
	# ST3, Python 3
	from html.parser import HTMLParser

class EcsstractorCommand(sublime_plugin.WindowCommand):
	def run(self):

		view = self.window.active_view()

		plugin_settings = sublime.load_settings('eCSStractor.sublime-settings')
		bem_nesting = plugin_settings.get('bem_nesting')
		self.brackets = plugin_settings.get('brackets')

		syntax = 'Packages/CSS/CSS.tmLanguage'

		# if view have any selection then work with selection, else with whole view
		selection = view.sel()[0]

		if len(selection) > 0:

			for sel in view.sel():
				region = sublime.Region(
					view.line(min(sel.a, sel.b)).a,  # line start of first line
					view.line(max(sel.a, sel.b)).b   # line end of last line
				)

		else:
			region = sublime.Region(0, view.size())

		self.source = view.substr(region)

		if bem_nesting:
			output = self.generateBEM()

			# set sass syntax if proper package is installed
			scss_syntax = os.path.join(sublime.packages_path(), 'Syntax Highlighting for Sass', 'Syntaxes', 'SCSS.tmLanguage')

			if os.path.exists(scss_syntax):

				syntax = 'Packages/Syntax Highlighting for Sass/Syntaxes/SCSS.tmLanguage'

		else:
			output = self.generateOutput()

		# if output not empty
		if output:
			# create new view
			new_file = self.window.new_file()
			new_file.set_syntax_file(syntax)
			new_file.run_command("ecsstractor_insert", {"text": output})
		else:
			sublime.status_message("eCSStractor can't find any classes")

	def generateOutput(self):

		css_template = "selector {\n}"
		output = ""

		# parsing
		parsed = parser()
		parsed.feed(self.source)

		# format output
		for i in range(len(parsed.classes)):
			output += css_template.replace("selector", "." + parsed.classes[i]) + "\n"

		return output

	def generateBEM(self):

		plugin_settings = sublime.load_settings('eCSStractor.sublime-settings')
		indentation = plugin_settings.get('indentation', '\t')
		element_separator = plugin_settings.get('bem.element_separator', '__')
		modifier_separator = plugin_settings.get('bem.modifier_separator', '--')
		parent_symbol = plugin_settings.get('preprocessor.parent_symbol', '&')

		output = ""
		selectors = []

		# parsing
		parsed = parser()
		parsed.feed(self.source)

		# build tree
		for i in range(len(parsed.classes)):
			selector = parsed.classes[i]

			block = {}
			element = {}

			# if block has element
			if element_separator in selector:

				parts = selector.split(element_separator)

				# check if block with this name exist already
				hasBlock = self.hasChild(selectors, "name", parts[0])

				# if block is exist link to list
				if hasBlock is not False:
					block = selectors[hasBlock]

				# if block is not exist give it name
				if hasBlock is False:
					block["name"] = parts[0]

				# if elements list exist in block
				if "elements" not in block:
					block["elements"] = []

				# get element and his modifier
				elementParts = parts[1].split(modifier_separator)

				# check if element with this name exist in block already
				hasElement = self.hasChild(block["elements"], "name", elementParts[0])

				# if element is exist link to list
				if hasElement is not False:
					element = block["elements"][hasElement]

				# if element is not exist give it name
				if hasElement is False:
					element["name"] = elementParts[0]

				# if element has modifier
				if len(elementParts) > 1:

					# if modifiers list exist in element
					if "modifiers" not in element:
						element["modifiers"] = []

					# add modifier
					element["modifiers"].append(elementParts[1])

				# if it is new element add it to block
				if hasElement is False:
					block["elements"].append(element)

				# if it is new block add it to list
				if hasBlock is False:
					selectors.append(block)

			# if block has modifier
			elif modifier_separator in selector:

				parts = selector.split(modifier_separator)

				hasBlock = self.hasChild(selectors, "name", parts[0])

				if hasBlock is not False:
					block = selectors[hasBlock]

				if hasBlock is False:
					block["name"] = parts[0]

				if "modifiers" not in block:
					block["modifiers"] = []

				block["modifiers"].append(parts[1])

				if hasBlock is False:
					selectors.append(block)

			else:

				hasBlock = self.hasChild(selectors, "name", selector)

				if hasBlock is False:
					block["name"] = selector
					selectors.append(block)

		# format output
		for block in selectors:

			if self.brackets:
				output += "." + block["name"] + " {\n"
			else:
				output += "." + block["name"] + "\n"

			indent = indentation
			indent1 = indent * 1
			indent2 = indent * 2

			if "modifiers" in block:

				for modifier in block["modifiers"]:
					if self.brackets:
						output += indent1 + parent_symbol + modifier_separator + modifier + " {\n"
						output += indent1 + "}\n"
					else:
						output += indent1 + parent_symbol + modifier_separator + modifier + "\n"
						output += "\n"

			if "elements" in block:

				for element in block["elements"]:
					if self.brackets:
						output += indent1 + parent_symbol + element_separator + element["name"] + " {\n"
					else:
						output += indent1 + parent_symbol + element_separator + element["name"] + "\n"

					if "modifiers" in element:

						for modifier in element["modifiers"]:
							if self.brackets:
								output += indent2 + parent_symbol + modifier_separator + modifier + " {\n"
								output += indent2 + "}\n"
							else:
								output += indent2 + parent_symbol + modifier_separator + modifier + "\n"
								output += "\n"

					if self.brackets:
						output += indent1 + "}\n"
					else:
						output += "\n"

			if self.brackets:
				output += "}\n"
			else:
				output += "\n"

		if not self.brackets:
			output = output.replace("\n\n\n\n", "\n\n")
			output = output.replace("\n\n\n", "\n\n")

		return output

	# check existance of key_name:key in listo
	def hasChild(self, listo, key_name, key):

		for y in range(len(listo)):
			if listo[y][key_name] == key:
				return y

		return False

class EcsstractorInsertCommand(sublime_plugin.TextCommand):
	def run(self, edit, text):
		self.view.insert(edit, 0, text)

class parser(HTMLParser):
	def __init__(self):
		HTMLParser.__init__(self)
		self.classes = []

	def handle_starttag(self, tag, attrs):

		for name, value in attrs:

			if name == "class":

				# remove whitespaces before and after string
				value = value.strip();

				# if class="" not empty
				if len(value) > 0:

					# split class string by whitespaces, in case multiple classes presented
					elementClasses = re.split("\s+", value)

					for i in range(len(elementClasses)):

						# add class to list if it's already not there
						if elementClasses[i] not in self.classes:
							self.classes.append(elementClasses[i])
