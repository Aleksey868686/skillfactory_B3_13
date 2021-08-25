class HTML:
    def __init__(self, output = None):
        self.output = output
        self.children = []
    
    def __iadd__(self, other):
        self.children.append(other)
        return self  
    
    def __enter__(self):
        return self
    
    def __exit__ (self, *args, **kwargs):
        if self.output is not None:
            with open(self.output, "w") as fp:
                fp.write(str(self))
        else:
            print(self)

    def __str__(self):
        html = "<html>\n"
        for child in self.children:
            html += str(child)
        html += "\n</html>"
        return html


class TopLevelTag:
    def __init__(self, tag_name):
        self.tag_name = tag_name
        self.children = []

    def __iadd__(self, other):
        self.children.append(other)
        return self  
    
    def __enter__(self):
        return self
    
    def __exit__ (self, *args, **kwargs):
        pass
    
    def __str__(self):
        html = f'<{self.tag_name}>\n'
        for child in self.children:
            html += str(child) 
        html += f'\n</{self.tag_name}>'
        return html


class Tag:
    def __init__(self, tag, klass=None, is_single=False, **kwargs):
        self.tag = tag  
        self.is_single = is_single
        self.text = ''
        self.attributes = {}
        self.children = []
        
        if klass is not None:
            self.attributes["class"] = " ".join(klass)


        for attr, value in kwargs.items():
            if "_" in attr:
                attr = attr.replace("_", "-")
            self.attributes[attr] = value
        
    def __enter__(self):
        return self

    def __exit__ (self, *args, **kwargs):
        pass
    
    def __iadd__(self, other):
        self.children.append(other)
        return self

    def __str__(self):
        attrs = []
        for attribute, value in self.attributes.items():
            attrs.append(f'{attribute}="{value}"')
        attrs = " ".join(attrs)

        if len(self.children) > 0:
            opening = f"<{self.tag} {attrs}>"
            if self.text:
                internal = f'{self.text}'
            else:
                internal = ""
            for child in self.children:
                internal += str(child)
            ending = f"</{self.tag}>"
            return opening + internal + ending
        else:
            if self.is_single:
                return f"<{self.tag} {attrs}/>"
            else:
                return f"<{self.tag} {attrs}>{self.text}</{self.tag}>"


if __name__ == "__main__":
  with HTML(output=None) as doc:
    with TopLevelTag("head") as head:
      with Tag("title") as title:
        title.text = "hello"
        head += title
      doc += head

    with TopLevelTag("body") as body:
      with Tag("h1", klass=("main-text",)) as h1:
        h1.text = "Test"
        body += h1

    with Tag("div", klass=("container", "container-fluid"), id="lead") as div:
      with Tag("p") as paragraph:
        paragraph.text = "another test"
        div += paragraph

      with Tag("img", is_single=True, src="/icon.png", data_image="responsive") as img:
        div += img

      body += div

    doc += body
