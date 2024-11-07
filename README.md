Overview:
PurduePrep is a web application which allows users to input study information from which they would like to find exam questions which cover similar content. PurduePrep finds relevant keywords from that input and generates a search query for its web crawler. The web crawler navigates though .edu website hits from the generated search query and finds the sites which are both the most relevant to the content and the most likely to contain exam style questions. Web scraping is then performed on these websites, and an NLP model locates the exam questions (if any) from these pages. These questions are then returned to the user on the PurduePrep website in response to their input.

Developers and Project Origin:
We (Josh Kamphuis, Seth Kricheff, and Emma Teff) started PurduePrep in August 2024 as a senior design project for Purdue University's ECE 49595 (Open Source Software). We as college studyents find answering past exam questions to be the most effective study method for midterms and final examinations, but if a professor does not provide past exams or they are not easily available online, we did not know how to find practice questions. PurduePrep solves that problem by doing the legwork of finding real exam questions across universities which cover the content a student wants to study. Thus, a student can study effectively even in courses which do not release practice exams.

User Guide:
Navigate to our hosted platform (https://purdue-prep-c2bdd7611c48.herokuapp.com/) to use PurduePrep as a study tool. Simply input content you'd like to study into our text box or upload a PDF or text file of course content. Once submitted, PurduePrep will find exam questions and return them on the website with links to where the questions were found included.

Getting Started as a Contributor:
See our API Documentation.
