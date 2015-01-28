# eCSStractor

Sublime Text plugin for extracting class names from HTML and generate CSS stylesheet for following work.

Default extracting:
![ecss_normal](https://cloud.githubusercontent.com/assets/654597/5896783/5ac44e42-a54c-11e4-8981-75456ac98f0b.gif)

With BEM nesting:
![ecss_bem](https://cloud.githubusercontent.com/assets/654597/5896785/60708c5c-a54c-11e4-963f-9e00ede168c3.gif)

## Usage

Open any document contain HTML and do one of the following:

* Press `Cmd+Shift+X` on Mac OS X or `Ctrl+Shift+X` on Windows/Linux.
* Go to `Tools → Run eCSStractor`
* Right click and select `Run eCSStractor`

Then you will see new tab with CSS selectors extracted from document.

Plugin can process either selected text or whole file.

## Options

The default settings can be viewed by accessing the **Preferences → Package Settings → eCSStractor → Settings – Default** menu entry. To ensure settings are not lost when the package is upgraded, make sure all edits are saved to **Settings – User**.

**brackets**

Add brackets. Useful for Sass syntax and Stylus.

_Default: **true**_

**bem_nesting**

BEM Nesting. Generate nested stylesheet for preprocessors rather simple stylesheet. You can see difference in _Example_ section of this readme.

_Default: **false**_

### Options only for BEM Nesting is on

**indentation**

Indentation.

_Default: **\t**_

**bem.element_separator**

Separator between block and element names.

_Default: ___

**bem.modifier_separator**

Separator between block or element and they modifier.

_Default: **--**_

**preprocessor.parent_symbol**

Parent symbol. Ex.: `&__element {}`

_Default: **&**_

## Example

Source:

```html
<ul class="nav nav--main">
    <li class="nav__item"><a href="" class="nav__link">Home</a></li>
    <li class="nav__item"><a href="" class="nav__link">Shop</a></li>
    <li class="nav__item"><a href="" class="nav__link nav__link--special">About</a></li>
</ul>
```

Run eCSStractor (BEM Nesting is off):

```css
.nav {
}
.nav--main {
}
.nav__item {
}
.nav__link {
}
.nav__link--special {
}
```

Run eCSStractor (BEM Nesting is on):

```scss
.nav {
    &--main {
    }
    &__item {
    }
    &__link {
        &--special {
        }
    }
}
```

# Installation

Most simple way it's install with [Package Control](https://packagecontrol.io/).

Open the Command Palette `Cmd+Shift+P` (OS X) or `Ctrl+Shift+P` (Linux/Windows) and select “Package Control: Install Package”, then search for `eCSStractor`.

# Similar tool

I've been inspired by [extractCSS](http://extractcss.com/) online tool. This tool have much more functions, but not very convenient for regular use.
