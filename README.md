# chess
Simple chess game being developed purely in python. GUI uses [pygame](http://www.pygame.org/) library.

Using some ideas from [Chess Programming Wiki](http://chessprogramming.wikispaces.com).

## Instructions
1. Make sure you have [Python](https://www.python.org/) and [pygame](http://www.pygame.org/) installed.
2. Run the chess engine via the GUI:
```bash
python gui.py
```
## GUI Hotkeys

- **C** - Change board [c]olor
- **E** - [E]valuate position
- **P** / **D** - [P]rint game info ([d]ump)
- **U** - [U]ndo move
- **H** - [H]elp (AI move)

## Screenshot
![chess game](http://i.imgur.com/110ZGeZ.png)

## Notable games
### First Man-vs-AI game:
```
1. e4 f6
2. d4 a5
3. Nf3 e6
4. Bc4 Ba3
5. Nxa3 e5
6. dxe5 fxe5
7. Nxe5 g6
8. h4 Qxh4
9. Rxh4 Na6
10. Bf7+ Ke7
11. Bg5+ Nf6
12. Rf4 h5
13. Bxf6+ Kf8
14. Bxh8 c5
15. Nxd7+ Bxd7
  (15. Nxg6#)
16. Qxd7 Nc7
  (16. Qd6#)
17. Qd6#
1-0
```
### First AI-vs-AI win:
```
1. d4 d6
2. e4 Nf6
3. Nc3 g6
4. f4 Bg7
5. Nf3 Bf8
6. Bb5+ c6
7. Be2 Ng4
8. h4 Nd7
9. Kf1 Qc7
10. Rb1 Rg8
11. a3 Nb6
12. Nd2 Nh6
13. Bd3 Be6
14. b4 Kd8
15. Ke1 Qc8
16. Nf1 Kd7
17. Bb2 Bg7
18. Rh2 Bxd4
19. g3 Rf8
20. Nb5 Bxb2
21. Rxb2 cxb5
22. Bxb5+ Kc7
23. Bd3 Qd7
24. Qc1 Qd8
25. Kd2 Rc8
26. Be2 Qd7
27. Bd1 a6
28. Ke1 Na8
29. Qd2 Rb8
30. Re2 f5
31. Qc3+ Kb6
32. Qe3+ Kc6
33. Qc3+ Kb6
34. Qe3+ Kb5
35. Qd3+ Kc6
36. exf5 Bf7
37. fxg6 hxg6
38. Kd2 Rfc8
39. Nh2 a5
40. bxa5 Rf8
41. Qe4+ Kc7
42. Qh1 Be8
43. Kc1 Nf7
44. Rg2 Nh6
45. Qe1 g5
46. fxg5 Nf7
47. Qc3+ Kd8
48. g6 Nh6
49. g7 Rg8
50. Qe3 Nf7
51. a4 Qxa4
52. Qd3 Rxg7
53. Qe3 Qxa5
54. h5 Qa1+
55. Kd2 Qxb2
56. Qe4 d5
57. Qxd5+ Bd7
58. Qa5+ Nb6
59. h6 Qd4+
60. Ke2 Qe4+
61. Kf1 Qc4+
62. Kg1 Qd4+
63. Kh1 Qxd1+
64. Nf1 Qxf1+
65. Rg1 Qh3#
0-1
```
