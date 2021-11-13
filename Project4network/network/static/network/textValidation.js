/**
 * This js file will be downloaded only when the user is authenticated.
 * This file is responsible for the validation of the text
 */

console.log('textValidation.js: user is authenticated');

class TextValidation {
  constructor(text) {
    this.text = text;
  }

  isValidText() {
    if (this.text.length === 0 || this.text.length > 280) {
      return false;
    }
    return true;
  }
}
