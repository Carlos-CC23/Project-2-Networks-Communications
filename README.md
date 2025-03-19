# Project-2-Networks-Communications

When converting binary data (a string of 0’s and 1’s) into signals that can be transmitted over a physical link, we can use one of three common encoding schemes:

Non-Return to Zero (NRZ):
Each bit is directly mapped to a signal level. In our implementation, a 1 is represented by a “high” signal (we denote as 'H') and a 0 by a “low” signal (denoted as 'L'). Decoding is simply reversing this mapping.

Non-Return to Zero Inverted (NRZI):
In NRZI, the encoded signal depends on transitions. The rule is:

If the bit is 1, the sender makes a transition from the current signal.
If the bit is 0, the sender keeps the current signal.
An initial state must be assumed (we use 'L' in our example). When decoding, a transition between consecutive signal levels indicates a 1; if there’s no change, the bit is 0.

Manchester Encoding:
This method combines clock and data by splitting each bit time into two halves. The encoding is as follows:

A 0 is encoded as a low-to-high transition (first half low, second half high; we represent this as "L", "H").
A 1 is encoded as a high-to-low transition (first half high, second half low; represented as "H", "L").
To decode, the receiver reads the signal in pairs: "L,H" means 0 and "H,L" means 1.

-----------------------------------------------------------------------------------------------------------
How to run the code on VS Code:
-
-Warning, you'll need to create a virtual environment to run it and to install matplotlib since that's used to plot the signal for each encoding.
-
-Steps: 

You open the Command prompt terminal (CMD) and type in ".venv\Scripts\Activate" . 

Then "pip install matplotlib".


Next you type in "python strategies.py" into the same terminal and the program begin and follow the instructions.
