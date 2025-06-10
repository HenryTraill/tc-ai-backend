Create a minimal react app with.

```bash
npx create-react-router@latest
```

Then run `claude` and copy&paste the prompt.

# Claude code prompt

You are in a minimal react app.

We are creating an app for Tutors to show the lessons they have scheduled with students, and give them details on the progress of their students so they can teach better.

Use dummy data while building the app, but all the dummy data in a single file with async methods to "fetch" data so it's easy to replace with real API calls later.

Run `npm run typecheck` regularly to check for errors.

Before building pages, define the set of common components that will be used across the app, such as buttons, input fields, and cards. Then use these whenever possible to avoid duplication.

Use tailwindcss for styling.

The app should be clean and modern with no drop shadows or gradients, the background color should be light blue (#d5f3ff), and the cards, top menu and main page content should have white backgrounds. The text should be the "inter" font from google fonts.

## Overall layout

Convert this app to show a very minimal UI suitable for mobile or desktop with just:
* a title "TutorCruncher AI"
* a center aligned main navbar menu, containing: "Home", "Lessons", "Students", "Insights", "+" (drop down with "create lesson" and "create student")
* a cog for settings in the top right
* the main page content

The title, navbar, settings cog part should be full page width, the page content should have a max width of 800px.

## Home page

The home page should contain a summary of upcoming lessons and recently completed lessons. These lessons should shows as cards with max width 600px, centered and stacked vertically. Each cards should show: if it's upcoming or completed, title, which student it's with, and it's date, start time and duration.

Each card should be a link to the lesson page.

## Lessons page

Should show:
* a toggle to "future lessons", "passed lessons"
* a list of lessons, with same format as the home page, but with pagination

## Lesson details page

Should show:
* if the lesson is upcoming: a button to start recording the lesson.
* summary: title, which student it's with (link to that student), and it's date, start time and duration.
* if the lesson is upcoming: a proposed lesson structure
* if the lesson is completed: a summary of what was covered, the student's strengths & weaknesses, and tips for the tutor on how to improve their teaching, option to view a transcript of the lesson or view the video/recording of the lesson.

## Students page

Show should a list of cards in the same format, one card per student.

## Student details page

Show:
* their name, age, address
* a summary of their current progress
* a list of their past and upcoming lessons (same format as the lessons list)
