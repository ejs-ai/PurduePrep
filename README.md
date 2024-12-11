# PurduePrep

## Overview
PurduePrep is a web application that allows users to input study information to find exam questions covering similar content. PurduePrep identifies relevant keywords from the input and generates a search query for its web crawler. The web crawler navigates through `.edu` website results based on the generated search query and finds sites that are both highly relevant to the content and likely to contain exam-style questions. Web scraping is then performed on these websites, and an NLP model locates exam questions (if any) from these pages. These questions are then returned to the user on the PurduePrep website in response to their input.

## Developers and Project Origin
We, Josh Kamphuis, Seth Kricheff, and Emma Teff, started PurduePrep in August 2024 as a senior design project for Purdue University's ECE 49595 (Open Source Software). As college students, we find that answering past exam questions is one of the most effective ways to study for midterms and finals. However, if professors don’t provide past exams or if they are not easily accessible online, finding practice questions can be challenging. PurduePrep addresses this need by locating real exam questions from universities that cover the specific content a student wants to study. This enables students to study effectively even in courses that do not release practice exams.

## User Guide
Navigate to our hosted platform: [PurduePrep on Google Cloud](https://react-824914791442.us-central1.run.app/) to use PurduePrep as a study tool. Simply enter the content you'd like to study in the text box or upload a PDF or text file of course content. Once submitted, PurduePrep will find exam questions and display them on the website, with links to the sources where the questions were found.

## Getting Started as a Contributor
For contributor guidance, please refer to our [API Documentation].
