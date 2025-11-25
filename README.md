# Resolution
Allows students to visually explore how resolution proofs in logic work

{Deployed app}[https://resolution.streamlit.app/]

## Quickstart

To prove that (A v B) & (A v ~B) & (~A v B) & (~A v ~B) is a contradiction, begin by entering "{A, B} {A, ~B} {~A, B} {~A, ~B}" in the text box on the first page and hitting submit. To create the below proof of the contradiction, click on the buttons {A, B} and {~A, B}, then the buttons {A, ~B} and {~A, ~B}, then the buttons {B} and {~B}.

  
  1     {A, B}                       Input clause

  2     {~A, B}                      Input clause

  3     {A, ~B}                      Input clause

  4     {~A, ~B}                     Input clause

  5     {B}                        1,2 Resolution

  6     {~B}                       3,4 Resolution

  7     {}                         5,6 Resolution
