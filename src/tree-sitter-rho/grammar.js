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

    _expression: ($) => choice($.match_expr, $.fn, $.drop, $.apply, $._atom),

    apply: ($) => prec.left(1, seq($._atom, repeat1($._atom))),

    _atom: ($) => choice($.number, $.string, $.array, $.quote, $.identifier, $.primitive),

    quote: ($) => seq("&", $.identifier),

    drop: ($) => ".",

    fn: ($) =>
      prec(2, seq(
        "(", field("params", repeat1($.param)), ")",
        field("body", choice($.match_expr, $.block, $._expression, $.drop)),
      )),

    match_expr: ($) =>
      seq(
        "match",
        "{",
        repeat(seq($.match_case, optional($._sep))),
        "}",
      ),

    match_case: ($) =>
      seq(
        field("guard", $.block),
        field("body", $.block),
      ),

    param: ($) => $.identifier,

    block: ($) =>
      seq(
        "{",
        repeat(seq(optional($._expression), $._sep)),
        optional($._expression),
        "}",
      ),

    array: ($) => seq("[", repeat($._atom), "]"),

    string: ($) => seq(
      '"',
      repeat(choice(
        $.escape_sequence,
        /[^"\\]+/,
      )),
      '"',
    ),

    escape_sequence: ($) => /\\[\\\"nt0]/,

    number: ($) => /\d+(\.\d+)?/,

    identifier: ($) => /[a-zA-Z_][a-zA-Z0-9_]*/,

    primitive: ($) => choice("+", "-", "*", "/", ">", "<", "==", "!=", ">=", "<="),

    comment: ($) => seq("--", /.*/),
  },
});
