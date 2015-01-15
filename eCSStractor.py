import sublime
import sublime_plugin
import re
from html.parser import HTMLParser

class EcsstractorCommand(sublime_plugin.WindowCommand):
	def run(self):

		view = self.window.active_view()

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

		code = view.substr(region)

		# get processed data
		output = self.generateOutput(code)

		# create new view, set CSS syntax and paste output
		new_file = self.window.new_file()
		new_file.set_syntax_file('Packages/CSS/CSS.tmLanguage')
		new_file.run_command("ecsstractor_insert", {"text": output})

	def generateOutput(self, source = ""):

		css_template = "selector {\n}"
		output = ""

		# parsing
		parsed = parser()
		parsed.feed(source)

		# format output
		for i in range(len(parsed.classes)):
			output += css_template.replace("selector", "." + parsed.classes[i]) + "\n"

		return output

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
