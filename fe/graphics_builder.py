# -*- coding: utf-8 -*-
from lxml import etree
import pdb

class HTMLComponent(object):
    
    def __init__(self, tag, text, attributes, children):
        self.tag = tag
        self.attributes = attributes
        self.text = text
        self.children = children

    def get_root_code(self):
        root = etree.Element(self.tag)
        for key, value in self.attributes.items():
            root.set(key, value)
        root.text = self.text
        for child in self.children:
            root.append(HTMLComponent.get_node_tree(child))
        return etree.tostring(root, pretty_print=True)

    def get_html_code(self):
        return etree.tostring(HTMLComponent.get_node_tree(self), pretty_print=True)

    @staticmethod
    def get_node_tree(node):
        element = etree.Element(node.tag)
        for key, value in node.attributes.items():
            element.set(key, str(value))
        element.text = str(node.text)
        for child in node.children:
            element.append(HTMLComponent.get_node_tree(child))
        return element

class Div(HTMLComponent):
    def __init__(self, text="", attributes={}, children=[]):
        super(Div, self).__init__("div", text, attributes, children)

class Modal(Div):

    SMALL = "modal-sm "
    LARGE = "modal-lg "
    NARROW = "modal-narrow "

    def __init__(self, title="", attributes={}, body_item_list=[], footer_item_list=[], include_header=True, include_footer=True, include_close_btn=True, close_btn_text="Close"):
        self.content = Div(attributes={"class":"modal-content"})
        content_list = []
        if include_header:
            self.close_x = Button(attributes={"type":"button", "data-dismiss":"modal", "aria-hidden":"true"}, text="x")
            self.close_x.attributes["class"] = "close"
            self.header_title = H3(attributes={"class":"modal-title", "id":attributes.get("id", "") + "Label"}, text=title)
            self.header = Div(attributes={"class":"modal-header"}, children=[self.close_x, self.header_title])
            content_list.append(self.header)
        self.body = Div(attributes={"class":"modal-body"}, children=body_item_list)
        content_list.append(self.body)
        if include_footer:
            footer_children = footer_item_list if footer_item_list else []
            if include_close_btn:
                self.close_btn = Button(attributes={"type":"button", "data-dismiss":"modal"}, text=close_btn_text)
                footer_children.append(self.close_btn)
            self.footer = Div(attributes={"class":"modal-footer"}, children=footer_children)
            content_list.append(self.footer)
        self.content.children = content_list
        self.dialog = Div(attributes={"class":"modal-dialog "+attributes.get("class", ""), "style":attributes.get("style", "")}, children=[self.content])
        attributes["class"] = "modal fade"
        attributes["role"] = "dialog"
        attributes["tabindex"] = "-1"
        attributes["aria-hidden"] = "true"
        attributes["aria-labelledby"] = attributes.get("id", "") + "Label"
        super(Modal, self).__init__(text="", attributes=attributes, children=[self.dialog])

class Carousel(Div):
    def __init__(self, attributes={}, slide_img_src=[], slide_captions=[], controls=False, interval=0):
        attributes["class"] = "carousel slide "+attributes.get("class","")
        inner_items = Div(attributes={"class":"carousel-inner"})
        inner_items.children = []
        indicators = OL(attributes={"class":"carousel-indicators"})
        indicators.children = []
        for img_src in slide_img_src:
            counter = slide_img_src.index(img_src)
            li = LI()
            li.attributes = {"data-target":"#"+attributes.get("id", ""), "data-slide-to":str(counter)}
            item = Div(attributes={"class":"item"})
            if counter == 0:
                li.attributes["class"] = "active"
                item.attributes["class"] = "item active"
            item.children=[Img(attributes={"src":img_src, "style":"margin: 0 auto;"})]
            caption = slide_captions[counter] if len(slide_captions) > counter else None
            if caption:
                caption_div = Div(attributes={"class":"carousel-caption"})
                if caption.__class__.__base__.__name__ == "HTMLComponent":
                    caption_div.children = [caption]
                else:
                    caption_div.children = [H1(text=caption)]
                item.children.append(caption_div)
            indicators.children.append(li)
            inner_items.children.append(item)
        children = [indicators, inner_items]
        if controls:
            children.append(A(
                attributes={"class":"left carousel-control", "href":"#"+attributes.get("id", ""), "data-slide":"prev"},
                children=[Span(attributes={"class":Span.GLYPHICON+"glyphicon-chevron-left"})]
            ))
            children.append(A(
                attributes={"class":"right carousel-control", "href":"#"+attributes.get("id", ""), "data-slide":"next"},
                children=[Span(attributes={"class":Span.GLYPHICON+"glyphicon-chevron-right"})]
            ))
        if interval:
            children.append(Script(text="$('.carousel').carousel({interval: "+str(interval)+"});"))
        super(Carousel, self).__init__(text="", attributes=attributes, children=children)

class H1(HTMLComponent):
    def __init__(self, text="", attributes={}, children=[]):
        super(H1, self).__init__("h1", text, attributes, children)

class H2(HTMLComponent):
    def __init__(self, text="", attributes={}, children=[]):
        super(H2, self).__init__("h2", text, attributes, children)

class H3(HTMLComponent):
    def __init__(self, text="", attributes={}, children=[]):
        super(H3, self).__init__("h3", text, attributes, children)

class Label(HTMLComponent):
    def __init__(self, text="", attributes={}, children=[]):
        super(Label, self).__init__("label", text, attributes, children)

class P(HTMLComponent):

    TEXT_MUTED = "text-muted "
    TEXT_PRIMARY = "text-primary "
    TEXT_SUCCESS = "text-success "
    TEXT_INFO = "text-info "
    TEXT_WARNING = "text-warning "
    TEXT_DANGER = "text-danger "
    BG_PRIMARY = "bg-primary "
    BG_SUCCESS = "bg-success "
    BG_INFO = "bg-info "
    BG_WARNING = "bg-warning "
    BG_DANGER = "bg-danger "

    def __init__(self, text="", attributes={}, children=[]):
        super(P, self).__init__("p", text, attributes, children)

class Form(HTMLComponent):
    def __init__(self, text="", attributes={}, item_list=[]):
        attributes["role"] = "form"
        children = []
        if text:
            children.append(H3(text=text))
        for item in item_list:
            if item.__class__.__name__ == "FormGroup":
                children.append(item)
            if item.__class__.__name__ == "Button":
                children.append(item)
            elif item.__class__.__name__ == "Input" or item.__class__.__base__.__name__ == "Input":
                children.append(item)
            elif item.__class__.__name__ == "HTMLComponent" or item.__class__.__base__.__name__ == "HTMLComponent":
                children.append(item)
        super(Form, self).__init__("form", "", attributes, children)

class FormGroup(Div):
    def __init__(self, label="", input=None, help_block=""):
        if input.__class__.__name__ == "Input" or input.__class__.__base__.__name__ == "Input" or input.__class__.__name__ == "Select":
            self.input = input
            if label.__class__.__name__ == "Label":
                if "id" in self.input.attributes:
                    label.attributes["for"] = self.input.attributes["id"]
                label.attributes["class"] = "control-label "+label.attributes.get("class", "")
                self.label = label
            elif label.__class__.__name__ == "str":
                self.label = Label(text=label, attributes={"class":"control-label "})
                if "id" in self.input.attributes:
                    self.label.attributes["for"] = self.input.attributes["id"]
            if help_block.__class__.__name__ == "P":
                help_block.attributes["class"] = "help-block " + help_block.attributes.get("class", "")
                self.help_block = help_block
            elif help_block.__class__.__name__ == "str":
                self.help_block = P(text=help_block, attributes={"class":"help_block "})
            children = []
            if self.label:
                children.append(self.label)
            children.append(self.input)
            if self.help_block:
                children.append(self.help_block)
            super(FormGroup, self).__init__(text="", attributes={"class":"form-group"}, children=children)
        else:
            super(FormGroup, self).__init__(text="", attributes={"class":"form-group"}, children=[])

class Input(HTMLComponent):
    def __init__(self, text="", attributes={}, children=[]):
        super(Input, self).__init__("input", text, attributes, children)

class Checkbox(Input):
    def __init__(self, attributes={}):
        attributes["type"] = "checkbox"
        super(Checkbox, self).__init__(attributes=attributes)
class Radio(Input):
    def __init__(self, attributes={}):
        attributes["type"] = "radio"
        super(Radio, self).__init__(attributes=attributes)
class Text(Input):
    def __init__(self, attributes={}):
        attributes["type"] = "text"
        attributes["class"] = "form-control "+attributes.get("class","")
        super(Text, self).__init__(attributes=attributes)
class Password(Input):
    def __init__(self, attributes={}):
        attributes["type"] = "password"
        attributes["class"] = "form-control "+attributes.get("class","")
        super(Password, self).__init__(attributes=attributes)
class Hidden(Input):
    def __init__(self, attributes={}):
        attributes["type"] = "hidden"
        super(Hidden, self).__init__(attributes=attributes)

class Select(HTMLComponent):
    def __init__(self, text="", attributes={}, children=[]):
        attributes["class"] = "form-control "+attributes.get("class","")
        super(Select, self).__init__("select", text, attributes, children)

class Option(HTMLComponent):
    def __init__(self, text="", attributes={}, children=[]):
        super(Option, self).__init__("option", text, attributes, children)

class Button(HTMLComponent):

    BUTTON = "btn "
    DEFAULT = "btn-default "
    PRIMARY = "btn-primary "
    SUCCESS = "btn-success "
    INFO = "btn-info "
    WARNING = "btn-warning "
    DANGER = "btn-danger "
    LINK = "btn-link "
    BLOCK = "btn-block "
    LARGE = "btn-lg "

    def __init__(self, attributes={}, text="", children=[]):
        attributes["class"] = "btn " + attributes.get("class", "")
        super(Button, self).__init__("button", text, attributes, children)

class A(HTMLComponent):
    def __init__(self, text="", attributes={}, children=[]):
        super(A, self).__init__("a", text, attributes, children)

class Table(HTMLComponent):

    STRIPED = "table-striped "
    BORDERED = "table-bordered "
    HOVER = "table-hover "
    CONDENSED = "table-condensed "

    def __init__(self, text="", attributes={}, children=[]):
        attributes["class"] = "table " + attributes.get("class", "")
        super(Table, self).__init__("table", text, attributes, children)

class TBody(HTMLComponent):
    def __init__(self, text="", attributes={}, children=[]):
        super(TBody, self).__init__("tbody", text, attributes, children)

class THead(HTMLComponent):
    def __init__(self, text="", attributes={}, children=[]):
        super(THead, self).__init__("thead", text, attributes, children)

class TFoot(HTMLComponent):
    def __init__(self, text="", attributes={}, children=[]):
        super(TFoot, self).__init__("tfoot", text, attributes, children)

class TH(HTMLComponent):
    def __init__(self, text="", attributes={}, children=[]):
        super(TH, self).__init__("th", text, attributes, children)

class TR(HTMLComponent):

    ACTIVE = "active "
    SUCCESS = "success "
    INFO = "info "
    WARNING = "warning "
    DANGER = "danger "

    def __init__(self, text="", attributes={}, children=[]):
        super(TR, self).__init__("tr", text, attributes, children)

class TD(HTMLComponent):

    ACTIVE = "active "
    SUCCESS = "success "
    INFO = "info "
    WARNING = "warning "
    DANGER = "danger "

    def __init__(self, text="", attributes={}, children=[]):
        super(TD, self).__init__("td", text, attributes, children)
        
class Img(HTMLComponent):

    ROUNDED = "img-rounded "
    CIRCLE = "img-circle "
    THUMBNAIL = "img-thumbnail "

    def __init__(self, text="", attributes={}, children=[]):
        super(Img, self).__init__("img", text, attributes, children)

class Span(HTMLComponent):

    LABEL_DEFAULT = "label label-default "
    LABLE_PRIMARY = "label label-primary "
    LABEL_SUCCESS = "label label-success "
    LABEL_INFO = "label label-info "
    LABEL_WARNING = "label label-warning "
    LABEL_DANGER = "label label-danger "
    BADGE = "badge "
    PULL_RIGHT = "pull-right "
    GLYPHICON = "glyphicon "

    def __init__(self, text="", attributes={}, children=[]):
        super(Span, self).__init__("span", text, attributes, children)

class OL(HTMLComponent):
    def __init__(self, text="", attributes={}, children=[]):
        super(OL, self).__init__("ol", text, attributes, children)

class LI(HTMLComponent):
    def __init__(self, text="", attributes={}, children=[]):
        super(LI, self).__init__("li", text, attributes, children)

class Script(HTMLComponent):
    def __init__(self, text="", attributes={}, children=[]):
        super(Script, self).__init__("script", text, attributes, children)

