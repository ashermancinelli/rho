(number) @number

(primitive) @operator

(identifier) @variable

(definition
  name: (identifier) @variable.definition)

(param
  (identifier) @variable.parameter)

(drop) @keyword

(comment) @comment

"<-" @keyword.operator
"(" @punctuation.bracket
")" @punctuation.bracket
"{" @punctuation.bracket
"}" @punctuation.bracket
