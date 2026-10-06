# FitBuddy

FitBuddy is a small Flask web application for collecting a user's basic fitness information and displaying a simple workout plan with general fitness tips.

> \*\*Important implementation note:\*\* The current repository does \*\*not\*\* actually call an AI model when a plan is generated. The `/plan` route constructs a fixed workout list and fixed tips in `main.py`. The separate `ai\_service.py` module contains a `generate\_fitness\_plan()` function, but that function is not imported or called by `main.py`.

## Features

* Home page with a link to create a plan.
* Fitness-plan form accepting name, age, goal, and fitness level.
* Plan result page displaying the submitted profile information, a fixed workout list, and fixed tips.
* History page placeholder.
* About page describing the intended AI-assisted purpose of the project.
* Jinja2 templates using a shared `base.html` layout.

## Requirements

The repository contains a `requirements` file with these packages:

* `Flask`
* `python-dotenv`
* `google-generativeai`

Only Flask is imported by the current application code. `python-dotenv` and `google-generativeai` are declared dependencies but are not used anywhere in the inspected source files.

The project does not pin package versions, so reproducible deployments should add explicit versions appropriate to the target environment.

## Project Structure

```text
FitBuddy1-main/
├── ai\_service.py
├── main.py
├── requirements
└── templates/
    ├── about.html
    ├── base.html
    ├── history.html
    ├── index.html
    └── plan.html
```

### `main.py`

Application entry point. Creates the Flask application and defines the four web routes:

* `GET /` → `home()`
* `GET /plan` and `POST /plan` → `plan()`
* `GET /history` → `history()`
* `GET /about` → `about()`

When executed directly, the module runs Flask with `debug=True`.

### `ai\_service.py`

Contains one standalone helper:

```python
generate\_fitness\_plan(name, age, goal, fitness\_level)
```

It returns a dictionary containing the supplied user information plus a fixed workout and fixed tips. It performs no model inference and has no external side effects.

### `templates/`

Jinja2 templates used by `render\_template()`.

`base.html` provides the common HTML shell, navigation, title block, content block, and references to `/static/css/style.css` and `/static/js/app.js`.

The supplied archive does **not** contain a `static/` directory, so those asset URLs are referenced by the templates but no matching files are included in the repository snapshot. The pages can still render, but those browser asset requests will not be served by this project as provided.

## Installation

### 1\. Create a virtual environment

Linux/macOS:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Windows PowerShell:

```powershell
py -m venv .venv
.\\.venv\\Scripts\\Activate.ps1
```

### 2\. Install dependencies

```bash
python -m pip install -r requirements
```

If your Python environment uses `python3` instead of `python`, use `python3 -m pip ...`.

## Running the Application

From the project root:

```bash
python main.py
```

The application starts through Flask's built-in development server. The source explicitly enables debug mode with:

```python
app.run(debug=True)
```

Open the local server address shown by Flask, normally:

```text
http://127.0.0.1:5000/
```

**Do not expose this debug development server to an untrusted or production environment.** Use a production WSGI server and disable debug mode for deployment.

## Using FitBuddy

### Home

Visit `/` and select **Create My Fitness Plan**. This takes you to `/plan`.

### Create a plan

Visit `/plan`.

The form accepts four fields:

|Field|HTML control|Required by browser|Accepted UI values|Server-side handling|
|-|-|-:|-|-|
|`name`|text|Yes|Free text|Read with `request.form.get()`|
|`age`|number|Yes|Numeric input in the browser UI|Read as a string; no numeric/range validation in Python|
|`goal`|select|Yes|`general fitness`, `strength`, `endurance`, `flexibility`|Passed through unchanged|
|`fitness\_level`|select|Yes|`beginner`, `intermediate`, `advanced`|Passed through unchanged|

Submitting the form sends a `POST` request to `/plan`.

The route then renders `plan.html` with:

* the submitted `name`
* the submitted `age`
* the submitted `goal`
* the submitted `fitness\_level`
* a fixed five-item workout list
* a fixed four-item tips list
* `generated=True`

The result page also provides **Create Another Plan**, which links back to `/plan` and therefore shows the form again.

## Generated Workout

The `/plan` route currently returns this fixed sequence:

1. Warm-up - 5 minutes
2. Bodyweight squats - 3 sets
3. Push-ups - 3 sets
4. Light cardio - 15 minutes
5. Cool-down - 5 minutes

The route also returns these fixed tips:

1. Stay hydrated.
2. Get enough sleep.
3. Take rest when needed.
4. Increase activity gradually.

The values of `goal` and `fitness\_level` are displayed to the user, but they do **not** currently alter the workout or tips.

## AI Service Behavior

`ai\_service.generate\_fitness\_plan()` builds this dictionary shape:

```python
{
    "name": name,
    "age": age,
    "goal": goal,
    "fitness\_level": fitness\_level,
    "workout": \[
        "Warm-up – 5 minutes",
        "Bodyweight squats – 3 sets",
        "Push-ups – 3 sets",
        "Walking or light cardio – 15 minutes",
        "Cool-down – 5 minutes",
    ],
    "tips": \[
        "Drink enough water.",
        "Get enough sleep.",
        "Take rest when needed.",
        "Increase activity gradually.",
    ],
}
```

There are two important details:

1. The function does not call Gemini, OpenAI, or any other AI service.
2. It uses slightly different wording from the fixed lists in `main.py` (for example, `Walking or light cardio` vs. `Light cardio`).

Because `main.py` never imports this function, its output is not used by the web application.

## Request Flow

```text
Browser
  |
  +--> GET / ---------> home() ---------> index.html
  |
  +--> GET /plan -----> plan() ---------> plan.html (form)
  |
  +--> POST /plan ----> plan() ---------> fixed workout + fixed tips
  |                                         |
  |                                         +--> plan.html (generated=True)
  |
  +--> GET /history --> history() -------> history.html
  |
  +--> GET /about ----> about() ---------> about.html
```

The current plan-generation path is entirely server-side and deterministic.

## Template Details

### `base.html`

Defines the common page structure and navigation. It provides Jinja blocks named `title` and `content`, and calls Flask's `url\_for()` to generate links for the route functions `home`, `plan`, `history`, and `about`.

It also asks Flask for these static assets:

* `static/css/style.css`
* `static/js/app.js`

Neither asset file exists in the supplied archive.

### `index.html`

Extends `base.html` and provides the landing page. It does not submit data itself; its main action links to `/plan`.

### `plan.html`

Uses the `generated` template variable as a two-state switch:

* `generated` false → display the form.
* `generated` true → display the generated plan.

When the generated plan is shown, the `workout` and `tips` values are iterated with Jinja `{% for %}` loops.

### `history.html`

Static placeholder with a link to the plan page.

### `about.html`

Static informational page.

## API / Route Reference

### `GET /`

Returns the home page.

### `GET /plan`

Returns the plan page in form mode by passing `generated=False`.

### `POST /plan`

Reads `name`, `age`, `goal`, and `fitness\_level` from `request.form`, creates the fixed workout/tips lists, and renders the result page.

No redirect, persistence, API call, model call, exception handling, or server-side validation is performed.

### `GET /history`

Returns the history placeholder page. No history is computed or loaded.

### `GET /about`

Returns the about page.

## Validation and Data Handling

The HTML form marks fields as required, which provides browser-side validation. This should not be confused with server-side validation.

The Python route uses:

```python
request.form.get("...")
```

If a client sends a request directly without one or more fields, `.get()` can return `None`, and the route still proceeds to render the response. There is no validation for:

* age range
* integer conversion of age
* allowed goal values
* allowed fitness-level values
* string length
* empty/whitespace-only names

For production use, these checks should be performed on the server.

## Security / Production Considerations

The supplied code is a learning/demo-style implementation. Before production deployment, consider at minimum:

* Disable `debug=True`.
* Add server-side input validation.
* Add CSRF protection for form submissions.
* Use a production WSGI server.
* Add structured error handling and logging.
* Decide whether plans should be persisted; implement a database/session layer if history is required.
* Remove unused dependencies or actually integrate the corresponding services.
* If an external AI service is added, keep API keys in environment variables and never hard-code secrets.
* Add tests for routes, validation, and plan generation.
* Provide the referenced `static/css/style.css` and `static/js/app.js`, or remove those references.

## Troubleshooting

### `ModuleNotFoundError: No module named 'flask'`

Install the dependencies in the active environment:

```bash
python -m pip install -r requirements
```

### Pages load but styling/scripts are missing

The archive contains no `static/` directory even though `base.html` references CSS and JavaScript files under `/static/`. Add the missing assets or remove the references.

### The history page is empty

This is expected from the current code. The application does not store generated plans anywhere.

### Changing the goal or fitness level does not change the workout

This is also expected from the current implementation. The selected values are displayed but do not drive any branching or AI generation logic.

### The application says it is AI-powered but the output is always the same

That is a source-code limitation, not a configuration issue. `main.py` does not invoke `ai\_service.py` or the `google-generativeai` package.

## Developer Notes

The repository has no test suite, no database schema, no configuration file, and no application factory. The Flask app object is created at module import time as `app = Flask(\_\_name\_\_)`.

The included `ai\_service.py` appears to be an early abstraction for plan generation, but it is currently disconnected from the route layer.

## License

No license file is included in the supplied archive. Licensing terms cannot be inferred from the source alone.

