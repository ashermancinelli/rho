package tree_sitter_rho_test

import (
	"testing"

	tree_sitter "github.com/tree-sitter/go-tree-sitter"
	tree_sitter_rho "github.com/tree-sitter/tree-sitter-rho/bindings/go"
)

func TestCanLoadGrammar(t *testing.T) {
	language := tree_sitter.NewLanguage(tree_sitter_rho.Language())
	if language == nil {
		t.Errorf("Error loading Rho grammar")
	}
}
