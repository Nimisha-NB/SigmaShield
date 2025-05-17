// The module 'vscode' contains the VS Code extensibility API
// Import the module and reference it with the alias vscode in your code below
const vscode = require("vscode");
const { extractApiKey } = require("./extractApiKey");
const { hideApiKey } = require("./hideApiKey");
// This method is called when your extension is activated
// Your extension is activated the very first time the command is executed

/**
 * @param {vscode.ExtensionContext} context
 */
function activate(context) {
  let hideCommand = vscode.commands.registerCommand(
    "extension.hideApiKey",
    function () {
      hideApiKey();
    }
  );

  let extractCommand = vscode.commands.registerCommand(
    "extension.extractApiKey",
    function () {
      extractApiKey();
    }
  );
  const disposable = vscode.commands.registerCommand(
    "Sigmashield.helloWorld",
    function () {
      // The code you place here will be executed every time your command is executed

      // Display a message box to the user
      vscode.window.showInformationMessage("Hello World from Sigmashield!");
    }
  );

  context.subscriptions.push(hideCommand, extractCommand, disposable);
}

// This method is called when your extension is deactivated
function deactivate() {}

module.exports = {
  activate,
  deactivate,
};
