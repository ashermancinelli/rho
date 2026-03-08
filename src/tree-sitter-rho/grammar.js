module.exports = grammar({
  name: "rho",

  extras: ($) => [/[ \t]/, $.comment],

  word: ($) => $.identifier,

  rules: {
    program: ($) =>
      seq(
        repeat(seq($._statement, $._sep)),
        optional($._statement),
      ),

    _sep: ($) => choice(/\n/, ";"),

    _statement: ($) => choice($.definition, $._expression),

    definition: ($) =>
      seq(field("name", $.identifier), "<-", field("body", $._expression)),

    _expression: ($) => choice($.fn, $.drop, $.apply, $._atom),

    apply: ($) => prec.left(1, seq($._atom, repeat1($._atom))),

    _atom: ($) => choice($.number, $.identifier, $.primitive),

    drop: ($) => ".",

    fn: ($) =>
      prec(2, seq(
        "(", field("params", repeat1($.param)), ")",
        field("body", choice($.block, $._expression, $.drop)),
      )),

    param: ($) => $.identifier,

    block: ($) =>
      seq(
        "{",
        repeat(seq(optional($._expression), $._sep)),
        optional($._expression),
        "}",
      ),

    number: ($) => /\d+(\.\d+)?/,

    identifier: ($) => /[a-zA-Z_][a-zA-Z0-9_]*/,

    primitive: ($) => choice("+", "-", "*", "/"),

    comment: ($) => seq("--", /.*/),
  },
});
