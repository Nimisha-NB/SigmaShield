const vscode = require("vscode");
const fs = require("fs");
const { PNG } = require("pngjs");

async function hideApiKey() {
  const fileUri = await vscode.window.showOpenDialog({
    canSelectMany: false,
    openLabel: "Select an image to embed Env Variables",
    filters: { Images: ["png"] },
  });

  if (!fileUri) {
    vscode.window.showErrorMessage("No image selected!");
    return;
  }

  const imagePath = fileUri[0].fsPath;

  const apiKey = await vscode.window.showInputBox({
    prompt: "Enter ENV Variables to embed",
  });

  if (!apiKey) {
    vscode.window.showErrorMessage("No Variables Key entered!");
    return;
  }

  // Pad the API key with whitespace to reach the standard length
  const paddedApiKey = apiKey.padEnd(1000, " ");

  // const outputPath = imagePath.replace(".png", "_hidden.png");

  fs.createReadStream(imagePath)
    .pipe(new PNG())
    .on("parsed", function () {
      for (let i = 0; i < paddedApiKey.length; i++) {
        this.data[i] = paddedApiKey.charCodeAt(i); // Embed padded API Key
      }
      this.pack()
        .pipe(fs.createWriteStream(imagePath))
        .on("finish", () => {
          vscode.window.showInformationMessage(
            `✅ ENV Variables hidden in: ${imagePath}`
          );
        })
        .on("error", (err) => {
          vscode.window.showErrorMessage(
            "❌ Error writing image: " + err.message
          );
        });
    })
    .on("error", (err) => {
      vscode.window.showErrorMessage("❌ Error reading image: " + err.message);
    });
}

module.exports = { hideApiKey };
