const vscode = require("vscode");
const fs = require("fs");
const path = require("path");
const { PNG } = require("pngjs");

async function extractApiKey() {
  const fileUri = await vscode.window.showOpenDialog({
    canSelectMany: false,
    openLabel: "Select an image to extract Env Variables",
    filters: { Images: ["png"] },
  });

  if (!fileUri) {
    vscode.window.showErrorMessage("No image selected!");
    return;
  }

  const imagePath = fileUri[0].fsPath;

  // const keyLength = await vscode.window.showInputBox({
  //   prompt: "Enter API Key Length",
  //   value: "100",
  // });

  const keyLength = 1000;

  if (!keyLength) {
    vscode.window.showErrorMessage("No length entered!");
    return;
  }

  fs.createReadStream(imagePath)
    .pipe(new PNG())
    .on("parsed", async function () {
      let extractedKey = "";
      // @ts-ignore
      for (let i = 0; i < parseInt(keyLength); i++) {
        extractedKey += String.fromCharCode(this.data[i]);
      }

      const trimmedKey = extractedKey.trim();

      const updatedKey = await vscode.window.showInputBox({
        prompt: "Modify the extracted API Key if needed",
        value: trimmedKey,
      });

      if (updatedKey !== null && updatedKey !== undefined) {
        // Create a completely new PNG to ensure no traces of old key remain
        const dirName = path.dirname(imagePath);
        const baseName = path.basename(imagePath, ".png");
        const newOutputPath = path.join(dirName, `${baseName}.png`);

        // Create a new PNG with the same dimensions but fresh data
        const newPng = new PNG({
          width: this.width,
          height: this.height,
          colorType: undefined,
          inputHasAlpha: true,
        });

        // Copy all the original image data
        for (let i = 0; i < this.data.length; i++) {
          newPng.data[i] = this.data[i];
        }

        // Clean the area where we'll store the key (complete reset)
        // @ts-ignore
        const cleanLength = parseInt(keyLength);
        for (let i = 0; i < cleanLength; i++) {
          newPng.data[i] = 32; // ASCII for space character (whitespace)
        }

        // Now embed the new key, padded with whitespace
        // @ts-ignore
        const paddedKey = updatedKey.padEnd(parseInt(keyLength), " ");
        const binaryKey = Buffer.from(paddedKey, "utf-8");
        for (let i = 0; i < binaryKey.length; i++) {
          newPng.data[i] = binaryKey[i];
        }

        // Write to the new file
        newPng
          .pack()
          .pipe(fs.createWriteStream(newOutputPath))
          .on("error", (err) => {
            vscode.window.showErrorMessage(
              "❌ Error writing image: " + err.message
            );
          });
      }
    })
    .on("error", (err) => {
      vscode.window.showErrorMessage("❌ Error reading image: " + err.message);
    });
}

module.exports = { extractApiKey };
