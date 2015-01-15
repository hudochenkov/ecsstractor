# eCSStractor

Sublime Text 3 plugin for extracting selectors from HTML and generate CSS stylesheet for following work. For now it's only extract classes.

## Usage

Open any document contain HTML and do one of the following:

* Press `Cmd+Shift+X` on Mac OS X or `Ctrl+Shift+X` on Windows/Linux.
* Go to `Tools → Run eCSStractor`
* Right click and select `Run eCSStractor`

Then you will see new tab with CSS selectors extracted from document.

Plugin can process either selected text or whole file.

## Example

Source:

```html
<ul class="nav">
    <li class="nav__item"><a href="" class="nav__link">Home</a></li>
    <li class="nav__item"><a href="" class="nav__link">Shop</a></li>
    <li class="nav__item"><a href="" class="nav__link nav__link--special">About</a></li>
</ul>
```

Run eCSStractor:

```css
.nav {
}
.nav__item {
}
.nav__link {
}
.nav__link--special {
}
```

# Installation

Via Package Control.

# Similar tool

I've been inspired by [extractCSS](http://extractcss.com/) online tool. This tool have much more functions, but not very convenient for regular use.