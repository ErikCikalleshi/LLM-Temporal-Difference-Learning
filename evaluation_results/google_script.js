function createFormWithSectionsFromSheet() {
  const conv = {
    c: function(text, obj) {
      return text.replace(new RegExp(`[${obj.reduce((s, {r}) => s += r, "")}]`, "g"), e => {
        const t = e.codePointAt(0);
        if ((t >= 48 && t <= 57) || (t >= 65 && t <= 90) || (t >= 97 && t <= 122)) {
          return obj.reduce((s, {r, d}) => {
            if (new RegExp(`[${r}]`).test(e)) s = String.fromCodePoint(e.codePointAt(0) + d);
            return s;
          }, "")
        }
        return e;
      })
    },
    bold: function(text) { return this.c(text, [{r: "0-9", d: 120734}, {r: "A-Z", d: 120211}, {r: "a-z", d: 120205}]); },
    italic: function(text) { return this.c(text, [{r: "A-Z", d: 120263}, {r: "a-z", d: 120257}]); },
    boldItalic: function(text) { return this.c(text, [{r: "A-Z", d: 120315}, {r: "a-z", d: 120309}]); }
  };

  var sheetId = '1gyDKSrQ1R4VFTge80aHbo_BD5a5hCDboYADcCW3b7CQ';
  var sheet = SpreadsheetApp.openById(sheetId).getSheets()[0];
  var data = sheet.getRange(2, 1, sheet.getLastRow() - 1, 7).getValues();
  data = shuffleArray(data);
  var form = FormApp.create('Historical Model Evaluation Survey');
  form.setConfirmationMessage('Thank you for your valuable feedback!');

  // Create a new Google Sheet to store the order of formatted text
  var newSheet = SpreadsheetApp.create('Formatted Text Order');
  var newSheetId = newSheet.getId();
  var newSheetData = [];
  // [sectionNumber, date, input, output, formattedText]
  newSheetData.push(["sectionNumber", "date", "input", "output", "formattedText"]); // Headers

  // Add introductory section with information
  form.addSectionHeaderItem()
      .setTitle(conv.bold('Welcome to the Historical Model Evaluation Survey'))
      .setHelpText(`
      
Dear Participant,

Thank you for participating in our survey for my bachelor's thesis. Your feedback will help evaluate a historical language model's accuracy and informativeness.

` +
conv.bold(`Research Objective:`) + `
Our research aims to assess the historical informativeness and fluency of a trained language model, similar to popular tools like ChatGPT. This model is designed to generate text that mimics the language style and content relevant to specific historical periods. Your evaluations will provide crucial insights into how well the model reflects historical facts and its ability to generate coherent, readable text that mirrors the style of the chosen era. 
In our case, the era will be before, between, or after `+ conv.bold("1987 - 2007") +`.

The ` + conv.bold(` bolded text `) + ` in the following passage is the prompt or starting point we provided to the model. The rest of the text is the model's generated continuation.

Your evaluation will guide improvements to this model.
` +
conv.italic(`\nNote that some outputs may not be historically accurate and might not make sense.\n`)

+ conv.boldItalic(`
Steps to follow:

1. Section Selection: Choose the section you were assigned.

2. Rate each response based on its historical informativeness and fluency.
`));

  // Add example scale items
  var examplePrompt = conv.bold("GOOD Example: George Washington ");
  var exampleResponse = "was the first President of the United States and a Founding Father.";
  var exampleLowScore = conv.bold("BAD Example: King George III ");
  var exampleLowResponse = "was an American patriot who fighted in Revolu. War was important very he good.";

  form.addSectionHeaderItem()
      .setTitle(examplePrompt + exampleResponse)
      .setHelpText(conv.italic('Example of high score: Accurate and informative'));

  form.addSectionHeaderItem()
      .setTitle(exampleLowScore + exampleLowResponse)
      .setHelpText(conv.italic('Example of low score: Inaccurate and not fluent'));

  form.addScaleItem()
      .setTitle('EXAMPLE - Historical Informativeness')
      .setBounds(1, 5)
      .setHelpText(conv.italic('Rate the value of the information. Consider aspects like relevance, helpfulness, accuracy, and focus.'))
      .setLabels('1 Bad', '5 Good');

  form.addScaleItem()
      .setTitle('EXAMPLE - Fluency')
      .setBounds(1, 5)
      .setHelpText(conv.italic('Rate how well the text flows and is easy to read. Consider aspects like grammar, coherence, and readability.'))
      .setLabels('1 Bad', '5 Good');

  form.addPageBreakItem();

  // Create the landing section
  var item = form.addMultipleChoiceItem();
  item.setTitle('Select the section you were instructed to complete:')
      .setRequired(true);

  var sectionNumber = 1;
  var sectionChoices = [];
  var pageBreaks = [];
  var help_text = conv.italic('Rate the value of the information. Consider aspects like relevance, helpfulness, accuracy, and focus.');
  var fluency_text = conv.italic('Rate how well the text flows and is easy to read. Consider aspects like grammar, coherence, and readability.');

  for (var i = 0; i < 24; i += 12) {
    var section = form.addPageBreakItem().setTitle('Section ' + sectionNumber);
    pageBreaks.push(section);
    sectionChoices.push(item.createChoice('Section ' + sectionNumber, section));

    data.slice(i, i + 12).forEach(function(row, index) {
      var input = row[0];
      var output = row[1];
      var date = row[6];
      if (input && output && date) {
        var cleanedOutput = output.replace(/<s>\[INST\].*?\[\/INST\]|\[INST:.*?\]/g, '').replace(input, '').trim();
        cleanedOutput = cleanedOutput.replace(/\n /g, ' ').replace(/\s+/g, ' ');
        input = conv.bold(input);
        var formattedText = input + " " + cleanedOutput;

        form.addSectionHeaderItem()
            .setTitle(formattedText);

        form.addScaleItem()
          .setTitle(`Historical Informativeness`)
          .setRequired(true)
          .setHelpText(help_text)
          .setBounds(1, 5)
          .setLabels('Very bad', 'Very good');

        form.addScaleItem()
          .setTitle(`Fluency`)
          .setRequired(true)
          .setHelpText(fluency_text)
          .setBounds(1, 5)
          .setLabels('Very bad', 'Very good');

        // Add formatted text and date to the new Google Sheet
        newSheetData.push([sectionNumber, date, input, output, formattedText]);
      }
    });
    sectionNumber++;
    section.setGoToPage(FormApp.PageNavigationType.SUBMIT);
  }

  item.setChoices(sectionChoices);

  Logger.log('Form created: ' + form.getPublishedUrl());

  // Write data to the new Google Sheet
  var newSheetRange = newSheet.getActiveSheet().getRange(1, 1, newSheetData.length, newSheetData[0].length);
  newSheetRange.setValues(newSheetData);

  // Log URL of the new Google Sheet
  Logger.log('New Google Sheet created: ' + newSheet.getUrl());
}

function shuffleArray(array) {
  for (var i = array.length - 1; i > 0; i--) {
    var j = Math.floor(Math.random() * (i + 1));
    var temp = array[i];
    array[i] = array[j];
    array[j] = temp;
  }
  return array;
}
