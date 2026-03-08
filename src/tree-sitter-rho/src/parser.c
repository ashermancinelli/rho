#include "tree_sitter/parser.h"

#if defined(__GNUC__) || defined(__clang__)
#pragma GCC diagnostic ignored "-Wmissing-field-initializers"
#endif

#define LANGUAGE_VERSION 14
#define STATE_COUNT 40
#define LARGE_STATE_COUNT 8
#define SYMBOL_COUNT 30
#define ALIAS_COUNT 0
#define TOKEN_COUNT 15
#define EXTERNAL_TOKEN_COUNT 0
#define FIELD_COUNT 3
#define MAX_ALIAS_SEQUENCE_LENGTH 4
#define PRODUCTION_ID_COUNT 3

enum ts_symbol_identifiers {
  sym_identifier = 1,
  anon_sym_LT_DASH = 2,
  anon_sym_LPAREN = 3,
  anon_sym_RPAREN = 4,
  anon_sym_LBRACE = 5,
  anon_sym_RBRACE = 6,
  sym_number = 7,
  anon_sym_PLUS = 8,
  anon_sym_DASH = 9,
  anon_sym_STAR = 10,
  anon_sym_SLASH = 11,
  anon_sym_DASH_DASH = 12,
  aux_sym_comment_token1 = 13,
  sym__newline = 14,
  sym_program = 15,
  sym__statement = 16,
  sym_definition = 17,
  sym__expression = 18,
  sym_apply = 19,
  sym__atom = 20,
  sym_fn = 21,
  sym_param = 22,
  sym_block = 23,
  sym_primitive = 24,
  sym_comment = 25,
  aux_sym_program_repeat1 = 26,
  aux_sym_apply_repeat1 = 27,
  aux_sym_fn_repeat1 = 28,
  aux_sym_block_repeat1 = 29,
};

static const char * const ts_symbol_names[] = {
  [ts_builtin_sym_end] = "end",
  [sym_identifier] = "identifier",
  [anon_sym_LT_DASH] = "<-",
  [anon_sym_LPAREN] = "(",
  [anon_sym_RPAREN] = ")",
  [anon_sym_LBRACE] = "{",
  [anon_sym_RBRACE] = "}",
  [sym_number] = "number",
  [anon_sym_PLUS] = "+",
  [anon_sym_DASH] = "-",
  [anon_sym_STAR] = "*",
  [anon_sym_SLASH] = "/",
  [anon_sym_DASH_DASH] = "--",
  [aux_sym_comment_token1] = "comment_token1",
  [sym__newline] = "_newline",
  [sym_program] = "program",
  [sym__statement] = "_statement",
  [sym_definition] = "definition",
  [sym__expression] = "_expression",
  [sym_apply] = "apply",
  [sym__atom] = "_atom",
  [sym_fn] = "fn",
  [sym_param] = "param",
  [sym_block] = "block",
  [sym_primitive] = "primitive",
  [sym_comment] = "comment",
  [aux_sym_program_repeat1] = "program_repeat1",
  [aux_sym_apply_repeat1] = "apply_repeat1",
  [aux_sym_fn_repeat1] = "fn_repeat1",
  [aux_sym_block_repeat1] = "block_repeat1",
};

static const TSSymbol ts_symbol_map[] = {
  [ts_builtin_sym_end] = ts_builtin_sym_end,
  [sym_identifier] = sym_identifier,
  [anon_sym_LT_DASH] = anon_sym_LT_DASH,
  [anon_sym_LPAREN] = anon_sym_LPAREN,
  [anon_sym_RPAREN] = anon_sym_RPAREN,
  [anon_sym_LBRACE] = anon_sym_LBRACE,
  [anon_sym_RBRACE] = anon_sym_RBRACE,
  [sym_number] = sym_number,
  [anon_sym_PLUS] = anon_sym_PLUS,
  [anon_sym_DASH] = anon_sym_DASH,
  [anon_sym_STAR] = anon_sym_STAR,
  [anon_sym_SLASH] = anon_sym_SLASH,
  [anon_sym_DASH_DASH] = anon_sym_DASH_DASH,
  [aux_sym_comment_token1] = aux_sym_comment_token1,
  [sym__newline] = sym__newline,
  [sym_program] = sym_program,
  [sym__statement] = sym__statement,
  [sym_definition] = sym_definition,
  [sym__expression] = sym__expression,
  [sym_apply] = sym_apply,
  [sym__atom] = sym__atom,
  [sym_fn] = sym_fn,
  [sym_param] = sym_param,
  [sym_block] = sym_block,
  [sym_primitive] = sym_primitive,
  [sym_comment] = sym_comment,
  [aux_sym_program_repeat1] = aux_sym_program_repeat1,
  [aux_sym_apply_repeat1] = aux_sym_apply_repeat1,
  [aux_sym_fn_repeat1] = aux_sym_fn_repeat1,
  [aux_sym_block_repeat1] = aux_sym_block_repeat1,
};

static const TSSymbolMetadata ts_symbol_metadata[] = {
  [ts_builtin_sym_end] = {
    .visible = false,
    .named = true,
  },
  [sym_identifier] = {
    .visible = true,
    .named = true,
  },
  [anon_sym_LT_DASH] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_LPAREN] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_RPAREN] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_LBRACE] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_RBRACE] = {
    .visible = true,
    .named = false,
  },
  [sym_number] = {
    .visible = true,
    .named = true,
  },
  [anon_sym_PLUS] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_DASH] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_STAR] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_SLASH] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_DASH_DASH] = {
    .visible = true,
    .named = false,
  },
  [aux_sym_comment_token1] = {
    .visible = false,
    .named = false,
  },
  [sym__newline] = {
    .visible = false,
    .named = true,
  },
  [sym_program] = {
    .visible = true,
    .named = true,
  },
  [sym__statement] = {
    .visible = false,
    .named = true,
  },
  [sym_definition] = {
    .visible = true,
    .named = true,
  },
  [sym__expression] = {
    .visible = false,
    .named = true,
  },
  [sym_apply] = {
    .visible = true,
    .named = true,
  },
  [sym__atom] = {
    .visible = false,
    .named = true,
  },
  [sym_fn] = {
    .visible = true,
    .named = true,
  },
  [sym_param] = {
    .visible = true,
    .named = true,
  },
  [sym_block] = {
    .visible = true,
    .named = true,
  },
  [sym_primitive] = {
    .visible = true,
    .named = true,
  },
  [sym_comment] = {
    .visible = true,
    .named = true,
  },
  [aux_sym_program_repeat1] = {
    .visible = false,
    .named = false,
  },
  [aux_sym_apply_repeat1] = {
    .visible = false,
    .named = false,
  },
  [aux_sym_fn_repeat1] = {
    .visible = false,
    .named = false,
  },
  [aux_sym_block_repeat1] = {
    .visible = false,
    .named = false,
  },
};

enum ts_field_identifiers {
  field_body = 1,
  field_name = 2,
  field_params = 3,
};

static const char * const ts_field_names[] = {
  [0] = NULL,
  [field_body] = "body",
  [field_name] = "name",
  [field_params] = "params",
};

static const TSFieldMapSlice ts_field_map_slices[PRODUCTION_ID_COUNT] = {
  [1] = {.index = 0, .length = 2},
  [2] = {.index = 2, .length = 2},
};

static const TSFieldMapEntry ts_field_map_entries[] = {
  [0] =
    {field_body, 2},
    {field_name, 0},
  [2] =
    {field_body, 3},
    {field_params, 1},
};

static const TSSymbol ts_alias_sequences[PRODUCTION_ID_COUNT][MAX_ALIAS_SEQUENCE_LENGTH] = {
  [0] = {0},
};

static const uint16_t ts_non_terminal_alias_map[] = {
  0,
};

static const TSStateId ts_primary_state_ids[STATE_COUNT] = {
  [0] = 0,
  [1] = 1,
  [2] = 2,
  [3] = 3,
  [4] = 4,
  [5] = 5,
  [6] = 6,
  [7] = 7,
  [8] = 8,
  [9] = 9,
  [10] = 10,
  [11] = 11,
  [12] = 12,
  [13] = 13,
  [14] = 14,
  [15] = 15,
  [16] = 16,
  [17] = 17,
  [18] = 18,
  [19] = 19,
  [20] = 20,
  [21] = 21,
  [22] = 22,
  [23] = 23,
  [24] = 24,
  [25] = 25,
  [26] = 26,
  [27] = 27,
  [28] = 28,
  [29] = 29,
  [30] = 30,
  [31] = 31,
  [32] = 32,
  [33] = 33,
  [34] = 34,
  [35] = 35,
  [36] = 36,
  [37] = 37,
  [38] = 38,
  [39] = 39,
};

static bool ts_lex(TSLexer *lexer, TSStateId state) {
  START_LEXER();
  eof = lexer->eof(lexer);
  switch (state) {
    case 0:
      if (eof) ADVANCE(3);
      ADVANCE_MAP(
        '\n', 21,
        '(', 5,
        ')', 6,
        '*', 14,
        '+', 12,
        '-', 13,
        '/', 15,
        '<', 1,
        '{', 7,
        '}', 8,
      );
      if (lookahead == '\t' ||
          lookahead == ' ') SKIP(0);
      if (('0' <= lookahead && lookahead <= '9')) ADVANCE(9);
      if (('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(11);
      END_STATE();
    case 1:
      if (lookahead == '-') ADVANCE(4);
      END_STATE();
    case 2:
      if (('0' <= lookahead && lookahead <= '9')) ADVANCE(10);
      END_STATE();
    case 3:
      ACCEPT_TOKEN(ts_builtin_sym_end);
      END_STATE();
    case 4:
      ACCEPT_TOKEN(anon_sym_LT_DASH);
      END_STATE();
    case 5:
      ACCEPT_TOKEN(anon_sym_LPAREN);
      END_STATE();
    case 6:
      ACCEPT_TOKEN(anon_sym_RPAREN);
      END_STATE();
    case 7:
      ACCEPT_TOKEN(anon_sym_LBRACE);
      END_STATE();
    case 8:
      ACCEPT_TOKEN(anon_sym_RBRACE);
      END_STATE();
    case 9:
      ACCEPT_TOKEN(sym_number);
      if (lookahead == '.') ADVANCE(2);
      if (('0' <= lookahead && lookahead <= '9')) ADVANCE(9);
      END_STATE();
    case 10:
      ACCEPT_TOKEN(sym_number);
      if (('0' <= lookahead && lookahead <= '9')) ADVANCE(10);
      END_STATE();
    case 11:
      ACCEPT_TOKEN(sym_identifier);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(11);
      END_STATE();
    case 12:
      ACCEPT_TOKEN(anon_sym_PLUS);
      END_STATE();
    case 13:
      ACCEPT_TOKEN(anon_sym_DASH);
      if (lookahead == '-') ADVANCE(16);
      END_STATE();
    case 14:
      ACCEPT_TOKEN(anon_sym_STAR);
      END_STATE();
    case 15:
      ACCEPT_TOKEN(anon_sym_SLASH);
      END_STATE();
    case 16:
      ACCEPT_TOKEN(anon_sym_DASH_DASH);
      END_STATE();
    case 17:
      ACCEPT_TOKEN(anon_sym_DASH_DASH);
      if (lookahead != 0 &&
          lookahead != '\n') ADVANCE(20);
      END_STATE();
    case 18:
      ACCEPT_TOKEN(aux_sym_comment_token1);
      if (lookahead == '-') ADVANCE(19);
      if (lookahead == '\t' ||
          lookahead == ' ') ADVANCE(18);
      if (lookahead != 0 &&
          lookahead != '\t' &&
          lookahead != '\n') ADVANCE(20);
      END_STATE();
    case 19:
      ACCEPT_TOKEN(aux_sym_comment_token1);
      if (lookahead == '-') ADVANCE(17);
      if (lookahead != 0 &&
          lookahead != '\n') ADVANCE(20);
      END_STATE();
    case 20:
      ACCEPT_TOKEN(aux_sym_comment_token1);
      if (lookahead != 0 &&
          lookahead != '\n') ADVANCE(20);
      END_STATE();
    case 21:
      ACCEPT_TOKEN(sym__newline);
      END_STATE();
    default:
      return false;
  }
}

static bool ts_lex_keywords(TSLexer *lexer, TSStateId state) {
  START_LEXER();
  eof = lexer->eof(lexer);
  switch (state) {
    case 0:
      ACCEPT_TOKEN(ts_builtin_sym_end);
      END_STATE();
    default:
      return false;
  }
}

static const TSLexMode ts_lex_modes[STATE_COUNT] = {
  [0] = {.lex_state = 0},
  [1] = {.lex_state = 0},
  [2] = {.lex_state = 0},
  [3] = {.lex_state = 0},
  [4] = {.lex_state = 0},
  [5] = {.lex_state = 0},
  [6] = {.lex_state = 0},
  [7] = {.lex_state = 0},
  [8] = {.lex_state = 0},
  [9] = {.lex_state = 0},
  [10] = {.lex_state = 0},
  [11] = {.lex_state = 0},
  [12] = {.lex_state = 0},
  [13] = {.lex_state = 0},
  [14] = {.lex_state = 0},
  [15] = {.lex_state = 0},
  [16] = {.lex_state = 0},
  [17] = {.lex_state = 0},
  [18] = {.lex_state = 0},
  [19] = {.lex_state = 0},
  [20] = {.lex_state = 0},
  [21] = {.lex_state = 0},
  [22] = {.lex_state = 0},
  [23] = {.lex_state = 0},
  [24] = {.lex_state = 0},
  [25] = {.lex_state = 0},
  [26] = {.lex_state = 0},
  [27] = {.lex_state = 0},
  [28] = {.lex_state = 0},
  [29] = {.lex_state = 0},
  [30] = {.lex_state = 0},
  [31] = {.lex_state = 0},
  [32] = {.lex_state = 0},
  [33] = {.lex_state = 0},
  [34] = {.lex_state = 0},
  [35] = {.lex_state = 18},
  [36] = {.lex_state = 0},
  [37] = {.lex_state = 0},
  [38] = {.lex_state = 0},
  [39] = {(TSStateId)(-1)},
};

static const uint16_t ts_parse_table[LARGE_STATE_COUNT][SYMBOL_COUNT] = {
  [0] = {
    [sym_comment] = STATE(0),
    [ts_builtin_sym_end] = ACTIONS(1),
    [sym_identifier] = ACTIONS(1),
    [anon_sym_LT_DASH] = ACTIONS(1),
    [anon_sym_LPAREN] = ACTIONS(1),
    [anon_sym_RPAREN] = ACTIONS(1),
    [anon_sym_LBRACE] = ACTIONS(1),
    [anon_sym_RBRACE] = ACTIONS(1),
    [sym_number] = ACTIONS(1),
    [anon_sym_PLUS] = ACTIONS(1),
    [anon_sym_DASH] = ACTIONS(1),
    [anon_sym_STAR] = ACTIONS(1),
    [anon_sym_SLASH] = ACTIONS(1),
    [anon_sym_DASH_DASH] = ACTIONS(3),
    [sym__newline] = ACTIONS(1),
  },
  [1] = {
    [sym_program] = STATE(37),
    [sym__statement] = STATE(34),
    [sym_definition] = STATE(27),
    [sym__expression] = STATE(27),
    [sym_apply] = STATE(22),
    [sym__atom] = STATE(10),
    [sym_fn] = STATE(22),
    [sym_primitive] = STATE(13),
    [sym_comment] = STATE(1),
    [aux_sym_program_repeat1] = STATE(2),
    [ts_builtin_sym_end] = ACTIONS(5),
    [sym_identifier] = ACTIONS(7),
    [anon_sym_LPAREN] = ACTIONS(9),
    [sym_number] = ACTIONS(11),
    [anon_sym_PLUS] = ACTIONS(13),
    [anon_sym_DASH] = ACTIONS(15),
    [anon_sym_STAR] = ACTIONS(13),
    [anon_sym_SLASH] = ACTIONS(13),
    [anon_sym_DASH_DASH] = ACTIONS(3),
  },
  [2] = {
    [sym__statement] = STATE(30),
    [sym_definition] = STATE(27),
    [sym__expression] = STATE(27),
    [sym_apply] = STATE(22),
    [sym__atom] = STATE(10),
    [sym_fn] = STATE(22),
    [sym_primitive] = STATE(13),
    [sym_comment] = STATE(2),
    [aux_sym_program_repeat1] = STATE(3),
    [ts_builtin_sym_end] = ACTIONS(17),
    [sym_identifier] = ACTIONS(7),
    [anon_sym_LPAREN] = ACTIONS(9),
    [sym_number] = ACTIONS(11),
    [anon_sym_PLUS] = ACTIONS(13),
    [anon_sym_DASH] = ACTIONS(15),
    [anon_sym_STAR] = ACTIONS(13),
    [anon_sym_SLASH] = ACTIONS(13),
    [anon_sym_DASH_DASH] = ACTIONS(3),
  },
  [3] = {
    [sym__statement] = STATE(36),
    [sym_definition] = STATE(27),
    [sym__expression] = STATE(27),
    [sym_apply] = STATE(22),
    [sym__atom] = STATE(10),
    [sym_fn] = STATE(22),
    [sym_primitive] = STATE(13),
    [sym_comment] = STATE(3),
    [aux_sym_program_repeat1] = STATE(3),
    [ts_builtin_sym_end] = ACTIONS(19),
    [sym_identifier] = ACTIONS(21),
    [anon_sym_LPAREN] = ACTIONS(24),
    [sym_number] = ACTIONS(27),
    [anon_sym_PLUS] = ACTIONS(30),
    [anon_sym_DASH] = ACTIONS(33),
    [anon_sym_STAR] = ACTIONS(30),
    [anon_sym_SLASH] = ACTIONS(30),
    [anon_sym_DASH_DASH] = ACTIONS(3),
  },
  [4] = {
    [sym__expression] = STATE(31),
    [sym_apply] = STATE(22),
    [sym__atom] = STATE(10),
    [sym_fn] = STATE(22),
    [sym_primitive] = STATE(13),
    [sym_comment] = STATE(4),
    [aux_sym_block_repeat1] = STATE(5),
    [sym_identifier] = ACTIONS(11),
    [anon_sym_LPAREN] = ACTIONS(9),
    [anon_sym_RBRACE] = ACTIONS(36),
    [sym_number] = ACTIONS(11),
    [anon_sym_PLUS] = ACTIONS(13),
    [anon_sym_DASH] = ACTIONS(15),
    [anon_sym_STAR] = ACTIONS(13),
    [anon_sym_SLASH] = ACTIONS(13),
    [anon_sym_DASH_DASH] = ACTIONS(3),
    [sym__newline] = ACTIONS(38),
  },
  [5] = {
    [sym__expression] = STATE(33),
    [sym_apply] = STATE(22),
    [sym__atom] = STATE(10),
    [sym_fn] = STATE(22),
    [sym_primitive] = STATE(13),
    [sym_comment] = STATE(5),
    [aux_sym_block_repeat1] = STATE(6),
    [sym_identifier] = ACTIONS(11),
    [anon_sym_LPAREN] = ACTIONS(9),
    [anon_sym_RBRACE] = ACTIONS(40),
    [sym_number] = ACTIONS(11),
    [anon_sym_PLUS] = ACTIONS(13),
    [anon_sym_DASH] = ACTIONS(15),
    [anon_sym_STAR] = ACTIONS(13),
    [anon_sym_SLASH] = ACTIONS(13),
    [anon_sym_DASH_DASH] = ACTIONS(3),
    [sym__newline] = ACTIONS(38),
  },
  [6] = {
    [sym__expression] = STATE(38),
    [sym_apply] = STATE(22),
    [sym__atom] = STATE(10),
    [sym_fn] = STATE(22),
    [sym_primitive] = STATE(13),
    [sym_comment] = STATE(6),
    [aux_sym_block_repeat1] = STATE(6),
    [sym_identifier] = ACTIONS(42),
    [anon_sym_LPAREN] = ACTIONS(45),
    [anon_sym_RBRACE] = ACTIONS(48),
    [sym_number] = ACTIONS(42),
    [anon_sym_PLUS] = ACTIONS(50),
    [anon_sym_DASH] = ACTIONS(53),
    [anon_sym_STAR] = ACTIONS(50),
    [anon_sym_SLASH] = ACTIONS(50),
    [anon_sym_DASH_DASH] = ACTIONS(3),
    [sym__newline] = ACTIONS(56),
  },
  [7] = {
    [sym__expression] = STATE(25),
    [sym_apply] = STATE(22),
    [sym__atom] = STATE(10),
    [sym_fn] = STATE(22),
    [sym_block] = STATE(25),
    [sym_primitive] = STATE(13),
    [sym_comment] = STATE(7),
    [sym_identifier] = ACTIONS(11),
    [anon_sym_LPAREN] = ACTIONS(9),
    [anon_sym_LBRACE] = ACTIONS(59),
    [sym_number] = ACTIONS(11),
    [anon_sym_PLUS] = ACTIONS(13),
    [anon_sym_DASH] = ACTIONS(15),
    [anon_sym_STAR] = ACTIONS(13),
    [anon_sym_SLASH] = ACTIONS(13),
    [anon_sym_DASH_DASH] = ACTIONS(3),
  },
};

static const uint16_t ts_small_parse_table[] = {
  [0] = 9,
    ACTIONS(3), 1,
      anon_sym_DASH_DASH,
    ACTIONS(15), 1,
      anon_sym_DASH,
    STATE(8), 1,
      sym_comment,
    STATE(11), 1,
      aux_sym_apply_repeat1,
    STATE(12), 1,
      sym__atom,
    STATE(13), 1,
      sym_primitive,
    ACTIONS(11), 2,
      sym_number,
      sym_identifier,
    ACTIONS(13), 3,
      anon_sym_PLUS,
      anon_sym_STAR,
      anon_sym_SLASH,
    ACTIONS(61), 3,
      ts_builtin_sym_end,
      anon_sym_RBRACE,
      sym__newline,
  [33] = 10,
    ACTIONS(3), 1,
      anon_sym_DASH_DASH,
    ACTIONS(9), 1,
      anon_sym_LPAREN,
    ACTIONS(15), 1,
      anon_sym_DASH,
    STATE(9), 1,
      sym_comment,
    STATE(10), 1,
      sym__atom,
    STATE(13), 1,
      sym_primitive,
    STATE(32), 1,
      sym__expression,
    ACTIONS(11), 2,
      sym_number,
      sym_identifier,
    STATE(22), 2,
      sym_apply,
      sym_fn,
    ACTIONS(13), 3,
      anon_sym_PLUS,
      anon_sym_STAR,
      anon_sym_SLASH,
  [68] = 9,
    ACTIONS(3), 1,
      anon_sym_DASH_DASH,
    ACTIONS(15), 1,
      anon_sym_DASH,
    STATE(8), 1,
      aux_sym_apply_repeat1,
    STATE(10), 1,
      sym_comment,
    STATE(12), 1,
      sym__atom,
    STATE(13), 1,
      sym_primitive,
    ACTIONS(11), 2,
      sym_number,
      sym_identifier,
    ACTIONS(13), 3,
      anon_sym_PLUS,
      anon_sym_STAR,
      anon_sym_SLASH,
    ACTIONS(63), 3,
      ts_builtin_sym_end,
      anon_sym_RBRACE,
      sym__newline,
  [101] = 8,
    ACTIONS(3), 1,
      anon_sym_DASH_DASH,
    ACTIONS(73), 1,
      anon_sym_DASH,
    STATE(12), 1,
      sym__atom,
    STATE(13), 1,
      sym_primitive,
    ACTIONS(67), 2,
      sym_number,
      sym_identifier,
    STATE(11), 2,
      sym_comment,
      aux_sym_apply_repeat1,
    ACTIONS(65), 3,
      ts_builtin_sym_end,
      anon_sym_RBRACE,
      sym__newline,
    ACTIONS(70), 3,
      anon_sym_PLUS,
      anon_sym_STAR,
      anon_sym_SLASH,
  [132] = 4,
    ACTIONS(3), 1,
      anon_sym_DASH_DASH,
    ACTIONS(78), 1,
      anon_sym_DASH,
    STATE(12), 1,
      sym_comment,
    ACTIONS(76), 8,
      ts_builtin_sym_end,
      anon_sym_RBRACE,
      sym_number,
      sym_identifier,
      anon_sym_PLUS,
      anon_sym_STAR,
      anon_sym_SLASH,
      sym__newline,
  [152] = 4,
    ACTIONS(3), 1,
      anon_sym_DASH_DASH,
    ACTIONS(82), 1,
      anon_sym_DASH,
    STATE(13), 1,
      sym_comment,
    ACTIONS(80), 8,
      ts_builtin_sym_end,
      anon_sym_RBRACE,
      sym_number,
      sym_identifier,
      anon_sym_PLUS,
      anon_sym_STAR,
      anon_sym_SLASH,
      sym__newline,
  [172] = 5,
    ACTIONS(3), 1,
      anon_sym_DASH_DASH,
    ACTIONS(82), 1,
      anon_sym_DASH,
    ACTIONS(84), 1,
      anon_sym_LT_DASH,
    STATE(14), 1,
      sym_comment,
    ACTIONS(80), 7,
      ts_builtin_sym_end,
      sym_number,
      sym_identifier,
      anon_sym_PLUS,
      anon_sym_STAR,
      anon_sym_SLASH,
      sym__newline,
  [194] = 4,
    ACTIONS(3), 1,
      anon_sym_DASH_DASH,
    ACTIONS(88), 1,
      anon_sym_DASH,
    STATE(15), 1,
      sym_comment,
    ACTIONS(86), 8,
      ts_builtin_sym_end,
      anon_sym_RBRACE,
      sym_number,
      sym_identifier,
      anon_sym_PLUS,
      anon_sym_STAR,
      anon_sym_SLASH,
      sym__newline,
  [214] = 4,
    ACTIONS(3), 1,
      anon_sym_DASH_DASH,
    ACTIONS(90), 1,
      anon_sym_DASH,
    STATE(16), 1,
      sym_comment,
    ACTIONS(48), 8,
      anon_sym_LPAREN,
      anon_sym_RBRACE,
      sym_number,
      sym_identifier,
      anon_sym_PLUS,
      anon_sym_STAR,
      anon_sym_SLASH,
      sym__newline,
  [234] = 4,
    ACTIONS(3), 1,
      anon_sym_DASH_DASH,
    ACTIONS(94), 1,
      anon_sym_DASH,
    STATE(17), 1,
      sym_comment,
    ACTIONS(92), 8,
      anon_sym_LPAREN,
      anon_sym_RBRACE,
      sym_number,
      sym_identifier,
      anon_sym_PLUS,
      anon_sym_STAR,
      anon_sym_SLASH,
      sym__newline,
  [254] = 4,
    ACTIONS(3), 1,
      anon_sym_DASH_DASH,
    ACTIONS(96), 1,
      anon_sym_DASH,
    STATE(18), 1,
      sym_comment,
    ACTIONS(19), 7,
      ts_builtin_sym_end,
      anon_sym_LPAREN,
      sym_number,
      sym_identifier,
      anon_sym_PLUS,
      anon_sym_STAR,
      anon_sym_SLASH,
  [273] = 6,
    ACTIONS(3), 1,
      anon_sym_DASH_DASH,
    ACTIONS(98), 1,
      sym_identifier,
    ACTIONS(100), 1,
      anon_sym_RPAREN,
    STATE(19), 1,
      sym_comment,
    STATE(20), 1,
      aux_sym_fn_repeat1,
    STATE(29), 1,
      sym_param,
  [292] = 5,
    ACTIONS(3), 1,
      anon_sym_DASH_DASH,
    ACTIONS(102), 1,
      sym_identifier,
    ACTIONS(105), 1,
      anon_sym_RPAREN,
    STATE(29), 1,
      sym_param,
    STATE(20), 2,
      sym_comment,
      aux_sym_fn_repeat1,
  [309] = 5,
    ACTIONS(3), 1,
      anon_sym_DASH_DASH,
    ACTIONS(98), 1,
      sym_identifier,
    STATE(19), 1,
      aux_sym_fn_repeat1,
    STATE(21), 1,
      sym_comment,
    STATE(29), 1,
      sym_param,
  [325] = 3,
    ACTIONS(3), 1,
      anon_sym_DASH_DASH,
    STATE(22), 1,
      sym_comment,
    ACTIONS(63), 3,
      ts_builtin_sym_end,
      anon_sym_RBRACE,
      sym__newline,
  [337] = 3,
    ACTIONS(3), 1,
      anon_sym_DASH_DASH,
    STATE(23), 1,
      sym_comment,
    ACTIONS(107), 3,
      ts_builtin_sym_end,
      anon_sym_RBRACE,
      sym__newline,
  [349] = 3,
    ACTIONS(3), 1,
      anon_sym_DASH_DASH,
    STATE(24), 1,
      sym_comment,
    ACTIONS(109), 3,
      ts_builtin_sym_end,
      anon_sym_RBRACE,
      sym__newline,
  [361] = 3,
    ACTIONS(3), 1,
      anon_sym_DASH_DASH,
    STATE(25), 1,
      sym_comment,
    ACTIONS(111), 3,
      ts_builtin_sym_end,
      anon_sym_RBRACE,
      sym__newline,
  [373] = 3,
    ACTIONS(3), 1,
      anon_sym_DASH_DASH,
    STATE(26), 1,
      sym_comment,
    ACTIONS(113), 3,
      ts_builtin_sym_end,
      anon_sym_RBRACE,
      sym__newline,
  [385] = 3,
    ACTIONS(3), 1,
      anon_sym_DASH_DASH,
    STATE(27), 1,
      sym_comment,
    ACTIONS(115), 2,
      ts_builtin_sym_end,
      sym__newline,
  [396] = 3,
    ACTIONS(3), 1,
      anon_sym_DASH_DASH,
    STATE(28), 1,
      sym_comment,
    ACTIONS(117), 2,
      anon_sym_RPAREN,
      sym_identifier,
  [407] = 3,
    ACTIONS(3), 1,
      anon_sym_DASH_DASH,
    STATE(29), 1,
      sym_comment,
    ACTIONS(119), 2,
      anon_sym_RPAREN,
      sym_identifier,
  [418] = 4,
    ACTIONS(3), 1,
      anon_sym_DASH_DASH,
    ACTIONS(121), 1,
      ts_builtin_sym_end,
    ACTIONS(123), 1,
      sym__newline,
    STATE(30), 1,
      sym_comment,
  [431] = 4,
    ACTIONS(3), 1,
      anon_sym_DASH_DASH,
    ACTIONS(40), 1,
      anon_sym_RBRACE,
    ACTIONS(125), 1,
      sym__newline,
    STATE(31), 1,
      sym_comment,
  [444] = 3,
    ACTIONS(3), 1,
      anon_sym_DASH_DASH,
    STATE(32), 1,
      sym_comment,
    ACTIONS(127), 2,
      ts_builtin_sym_end,
      sym__newline,
  [455] = 4,
    ACTIONS(3), 1,
      anon_sym_DASH_DASH,
    ACTIONS(125), 1,
      sym__newline,
    ACTIONS(129), 1,
      anon_sym_RBRACE,
    STATE(33), 1,
      sym_comment,
  [468] = 4,
    ACTIONS(3), 1,
      anon_sym_DASH_DASH,
    ACTIONS(17), 1,
      ts_builtin_sym_end,
    ACTIONS(123), 1,
      sym__newline,
    STATE(34), 1,
      sym_comment,
  [481] = 3,
    ACTIONS(131), 1,
      anon_sym_DASH_DASH,
    ACTIONS(133), 1,
      aux_sym_comment_token1,
    STATE(35), 1,
      sym_comment,
  [491] = 3,
    ACTIONS(3), 1,
      anon_sym_DASH_DASH,
    ACTIONS(123), 1,
      sym__newline,
    STATE(36), 1,
      sym_comment,
  [501] = 3,
    ACTIONS(3), 1,
      anon_sym_DASH_DASH,
    ACTIONS(135), 1,
      ts_builtin_sym_end,
    STATE(37), 1,
      sym_comment,
  [511] = 3,
    ACTIONS(3), 1,
      anon_sym_DASH_DASH,
    ACTIONS(125), 1,
      sym__newline,
    STATE(38), 1,
      sym_comment,
  [521] = 1,
    ACTIONS(137), 1,
      ts_builtin_sym_end,
};

static const uint32_t ts_small_parse_table_map[] = {
  [SMALL_STATE(8)] = 0,
  [SMALL_STATE(9)] = 33,
  [SMALL_STATE(10)] = 68,
  [SMALL_STATE(11)] = 101,
  [SMALL_STATE(12)] = 132,
  [SMALL_STATE(13)] = 152,
  [SMALL_STATE(14)] = 172,
  [SMALL_STATE(15)] = 194,
  [SMALL_STATE(16)] = 214,
  [SMALL_STATE(17)] = 234,
  [SMALL_STATE(18)] = 254,
  [SMALL_STATE(19)] = 273,
  [SMALL_STATE(20)] = 292,
  [SMALL_STATE(21)] = 309,
  [SMALL_STATE(22)] = 325,
  [SMALL_STATE(23)] = 337,
  [SMALL_STATE(24)] = 349,
  [SMALL_STATE(25)] = 361,
  [SMALL_STATE(26)] = 373,
  [SMALL_STATE(27)] = 385,
  [SMALL_STATE(28)] = 396,
  [SMALL_STATE(29)] = 407,
  [SMALL_STATE(30)] = 418,
  [SMALL_STATE(31)] = 431,
  [SMALL_STATE(32)] = 444,
  [SMALL_STATE(33)] = 455,
  [SMALL_STATE(34)] = 468,
  [SMALL_STATE(35)] = 481,
  [SMALL_STATE(36)] = 491,
  [SMALL_STATE(37)] = 501,
  [SMALL_STATE(38)] = 511,
  [SMALL_STATE(39)] = 521,
};

static const TSParseActionEntry ts_parse_actions[] = {
  [0] = {.entry = {.count = 0, .reusable = false}},
  [1] = {.entry = {.count = 1, .reusable = false}}, RECOVER(),
  [3] = {.entry = {.count = 1, .reusable = true}}, SHIFT(35),
  [5] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_program, 0, 0, 0),
  [7] = {.entry = {.count = 1, .reusable = true}}, SHIFT(14),
  [9] = {.entry = {.count = 1, .reusable = true}}, SHIFT(21),
  [11] = {.entry = {.count = 1, .reusable = true}}, SHIFT(13),
  [13] = {.entry = {.count = 1, .reusable = true}}, SHIFT(15),
  [15] = {.entry = {.count = 1, .reusable = false}}, SHIFT(15),
  [17] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_program, 1, 0, 0),
  [19] = {.entry = {.count = 1, .reusable = true}}, REDUCE(aux_sym_program_repeat1, 2, 0, 0),
  [21] = {.entry = {.count = 2, .reusable = true}}, REDUCE(aux_sym_program_repeat1, 2, 0, 0), SHIFT_REPEAT(14),
  [24] = {.entry = {.count = 2, .reusable = true}}, REDUCE(aux_sym_program_repeat1, 2, 0, 0), SHIFT_REPEAT(21),
  [27] = {.entry = {.count = 2, .reusable = true}}, REDUCE(aux_sym_program_repeat1, 2, 0, 0), SHIFT_REPEAT(13),
  [30] = {.entry = {.count = 2, .reusable = true}}, REDUCE(aux_sym_program_repeat1, 2, 0, 0), SHIFT_REPEAT(15),
  [33] = {.entry = {.count = 2, .reusable = false}}, REDUCE(aux_sym_program_repeat1, 2, 0, 0), SHIFT_REPEAT(15),
  [36] = {.entry = {.count = 1, .reusable = true}}, SHIFT(24),
  [38] = {.entry = {.count = 1, .reusable = true}}, SHIFT(17),
  [40] = {.entry = {.count = 1, .reusable = true}}, SHIFT(23),
  [42] = {.entry = {.count = 2, .reusable = true}}, REDUCE(aux_sym_block_repeat1, 2, 0, 0), SHIFT_REPEAT(13),
  [45] = {.entry = {.count = 2, .reusable = true}}, REDUCE(aux_sym_block_repeat1, 2, 0, 0), SHIFT_REPEAT(21),
  [48] = {.entry = {.count = 1, .reusable = true}}, REDUCE(aux_sym_block_repeat1, 2, 0, 0),
  [50] = {.entry = {.count = 2, .reusable = true}}, REDUCE(aux_sym_block_repeat1, 2, 0, 0), SHIFT_REPEAT(15),
  [53] = {.entry = {.count = 2, .reusable = false}}, REDUCE(aux_sym_block_repeat1, 2, 0, 0), SHIFT_REPEAT(15),
  [56] = {.entry = {.count = 2, .reusable = true}}, REDUCE(aux_sym_block_repeat1, 2, 0, 0), SHIFT_REPEAT(17),
  [59] = {.entry = {.count = 1, .reusable = true}}, SHIFT(4),
  [61] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_apply, 2, 0, 0),
  [63] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym__expression, 1, 0, 0),
  [65] = {.entry = {.count = 1, .reusable = true}}, REDUCE(aux_sym_apply_repeat1, 2, 0, 0),
  [67] = {.entry = {.count = 2, .reusable = true}}, REDUCE(aux_sym_apply_repeat1, 2, 0, 0), SHIFT_REPEAT(13),
  [70] = {.entry = {.count = 2, .reusable = true}}, REDUCE(aux_sym_apply_repeat1, 2, 0, 0), SHIFT_REPEAT(15),
  [73] = {.entry = {.count = 2, .reusable = false}}, REDUCE(aux_sym_apply_repeat1, 2, 0, 0), SHIFT_REPEAT(15),
  [76] = {.entry = {.count = 1, .reusable = true}}, REDUCE(aux_sym_apply_repeat1, 1, 0, 0),
  [78] = {.entry = {.count = 1, .reusable = false}}, REDUCE(aux_sym_apply_repeat1, 1, 0, 0),
  [80] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym__atom, 1, 0, 0),
  [82] = {.entry = {.count = 1, .reusable = false}}, REDUCE(sym__atom, 1, 0, 0),
  [84] = {.entry = {.count = 1, .reusable = true}}, SHIFT(9),
  [86] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_primitive, 1, 0, 0),
  [88] = {.entry = {.count = 1, .reusable = false}}, REDUCE(sym_primitive, 1, 0, 0),
  [90] = {.entry = {.count = 1, .reusable = false}}, REDUCE(aux_sym_block_repeat1, 2, 0, 0),
  [92] = {.entry = {.count = 1, .reusable = true}}, REDUCE(aux_sym_block_repeat1, 1, 0, 0),
  [94] = {.entry = {.count = 1, .reusable = false}}, REDUCE(aux_sym_block_repeat1, 1, 0, 0),
  [96] = {.entry = {.count = 1, .reusable = false}}, REDUCE(aux_sym_program_repeat1, 2, 0, 0),
  [98] = {.entry = {.count = 1, .reusable = true}}, SHIFT(28),
  [100] = {.entry = {.count = 1, .reusable = true}}, SHIFT(7),
  [102] = {.entry = {.count = 2, .reusable = true}}, REDUCE(aux_sym_fn_repeat1, 2, 0, 0), SHIFT_REPEAT(28),
  [105] = {.entry = {.count = 1, .reusable = true}}, REDUCE(aux_sym_fn_repeat1, 2, 0, 0),
  [107] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_block, 3, 0, 0),
  [109] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_block, 2, 0, 0),
  [111] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_fn, 4, 0, 2),
  [113] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_block, 4, 0, 0),
  [115] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym__statement, 1, 0, 0),
  [117] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_param, 1, 0, 0),
  [119] = {.entry = {.count = 1, .reusable = true}}, REDUCE(aux_sym_fn_repeat1, 1, 0, 0),
  [121] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_program, 2, 0, 0),
  [123] = {.entry = {.count = 1, .reusable = true}}, SHIFT(18),
  [125] = {.entry = {.count = 1, .reusable = true}}, SHIFT(16),
  [127] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_definition, 3, 0, 1),
  [129] = {.entry = {.count = 1, .reusable = true}}, SHIFT(26),
  [131] = {.entry = {.count = 1, .reusable = false}}, SHIFT(35),
  [133] = {.entry = {.count = 1, .reusable = false}}, SHIFT(39),
  [135] = {.entry = {.count = 1, .reusable = true}},  ACCEPT_INPUT(),
  [137] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_comment, 2, 0, 0),
};

#ifdef __cplusplus
extern "C" {
#endif
#ifdef TREE_SITTER_HIDE_SYMBOLS
#define TS_PUBLIC
#elif defined(_WIN32)
#define TS_PUBLIC __declspec(dllexport)
#else
#define TS_PUBLIC __attribute__((visibility("default")))
#endif

TS_PUBLIC const TSLanguage *tree_sitter_rho(void) {
  static const TSLanguage language = {
    .version = LANGUAGE_VERSION,
    .symbol_count = SYMBOL_COUNT,
    .alias_count = ALIAS_COUNT,
    .token_count = TOKEN_COUNT,
    .external_token_count = EXTERNAL_TOKEN_COUNT,
    .state_count = STATE_COUNT,
    .large_state_count = LARGE_STATE_COUNT,
    .production_id_count = PRODUCTION_ID_COUNT,
    .field_count = FIELD_COUNT,
    .max_alias_sequence_length = MAX_ALIAS_SEQUENCE_LENGTH,
    .parse_table = &ts_parse_table[0][0],
    .small_parse_table = ts_small_parse_table,
    .small_parse_table_map = ts_small_parse_table_map,
    .parse_actions = ts_parse_actions,
    .symbol_names = ts_symbol_names,
    .field_names = ts_field_names,
    .field_map_slices = ts_field_map_slices,
    .field_map_entries = ts_field_map_entries,
    .symbol_metadata = ts_symbol_metadata,
    .public_symbol_map = ts_symbol_map,
    .alias_map = ts_non_terminal_alias_map,
    .alias_sequences = &ts_alias_sequences[0][0],
    .lex_modes = ts_lex_modes,
    .lex_fn = ts_lex,
    .keyword_lex_fn = ts_lex_keywords,
    .keyword_capture_token = sym_identifier,
    .primary_state_ids = ts_primary_state_ids,
  };
  return &language;
}
#ifdef __cplusplus
}
#endif
