import XCTest
import SwiftTreeSitter
import TreeSitterRho

final class TreeSitterRhoTests: XCTestCase {
    func testCanLoadGrammar() throws {
        let parser = Parser()
        let language = Language(language: tree_sitter_rho())
        XCTAssertNoThrow(try parser.setLanguage(language),
                         "Error loading Rho grammar")
    }
}
