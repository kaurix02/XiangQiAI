import play
import sys

pls = play.players[1:]
print(play.run_test_sm(pls[int(sys.argv[1])], pls[int(sys.argv[2])],10))

