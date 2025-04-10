from flask import Flask, render_template, request
import spacy

app = Flask(__name__)
nlp = spacy.load("en_core_web_sm")

@app.route("/", methods=["GET", "POST"])
def index():
    entities = []
    raw_text = ""
    highlighted_text = ""
    
    if request.method == "POST":
        raw_text = request.form["text"]
        doc = nlp(raw_text)
        entities = [(ent.text, ent.label_) for ent in doc.ents]

        replacements = []
        for ent in doc.ents:
            replacement = f'<span class="entity-{ent.label_}" title="{ent.label_}">{ent.text}</span>'
            replacements.append((ent.start_char, ent.end_char, replacement))

        replacements.sort(reverse=True, key=lambda x: x[0])

        highlighted_text = raw_text
        for start, end, replacement in replacements:
            highlighted_text = highlighted_text[:start] + replacement + highlighted_text[end:]

        # Debug output
        print("Original text:", raw_text)
        print("Entities found:", entities)
        print("Highlighted text:", highlighted_text)

    return render_template("index.html", 
                           entities=entities, 
                           text=raw_text, 
                           highlighted_text=highlighted_text)

if __name__ == "__main__":
    app.run(debug=True)
