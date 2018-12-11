#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pprint import pprint


class SuffixTree:


    def __init__(self,T):
        self.bottom = "bottom"
        self.root = ""
        self.Qp = [self.bottom,self.root]
        self.gp = {self.root: {}}
        self.fp = {self.root: self.bottom}
        self.T = T
        self.algorithm2()


    def algorithm2(self):
        # Builds STree(T) for string T
        # one char at time
        # with one scan left to right
        s = self.root
        k = 0
        for i in range(len(self.T)):
            # i-th Endpoint is (i+1)-th Active Point
            (s,k) = self.update(s,(k,i))
            (s,k) = self.canonize(s,(k,i))


    def update(self,s,(k,i)):
        # Transforms STree(T(i-1)) into STree(T(i))
        # by inserting the ti-transitions in the second group:
        # from Active Point to Endpoint.
        # Returns a reference pair for sj' (the Endpoint)

        # (s,(k,i-1)) = reference pair for the Active Point

        ti = self.T[i]

        oldr = self.root

        (is_end_point,r) = self.testAndSplit(s,(k,i-1),ti)

        while not is_end_point:
            # create new state r'
            rp = r + str(i) + ti + "_"

            self.Qp.append(rp)
            self.updateGP(r,(i,len(self.T)-1),rp)

            if oldr != self.root:
                self.fp[oldr] = r
            oldr = r

            (s,k) = self.canonize(self.fp[s],(k,i-1))

            (is_end_point,r) = self.testAndSplit(s,(k,i-1),ti)

        if oldr != self.root:
            self.fp[oldr] = s

        return (s,k)


    def updateGP(self,s,kp,r):
        if s in self.gp:
            self.gp[s][kp] = r
        else:
            self.gp[s] = {kp: r}


    def getTransition(self,s,t):
        # Return the t-transition from s assuming it exists.
        if s == self.bottom:
            return ((-1,-1),self.root)
        for (kp,pp) in self.gp[s]:
            if self.T[kp] == t:
                sp = self.gp[s][(kp,pp)]
                return ((kp,pp),sp)


    def existsTransition(self,s,t):
        # Return True if the t-transition from s exists or False.
        if s == self.bottom:
            return True
        for (kp,pp) in self.gp[s]:
            if self.T[kp] == t:
                return True
        return False


    def testAndSplit(self,s,(k,p),t):
        # Tests whether or not a state with canonical reference pair (s,(k,p)) is the endpoint,
        # that is, a state that in STrie(T(i-1)) would have a ti-transition.
        # Symbol ti is given as input parameter t.
        # The test result is returned as the first output parameter.
        # If (s,(k,p)) is not the endpoint, then state (s,(k,p)) is made explicit (if not already so) by splitting a transition.
        # The explicit state is returned as the second output parameter.
        if k <= p:
            # s is implicit
            ((kp,pp),sp) = self.getTransition(s,self.T[k])

            # check if k' exists sometimes or is always just k
            if kp != k:
                print "Found k'=" + str(kp) + " (k=" + str(k) + ")"

            if t == self.T[kp + (p - k) + 1]:
                # endpoint
                return (True,s)
            else:
                # no endpoint
                del self.gp[s][(kp,pp)]
                # new state r
                r = s + str(kp) + self.T[kp:kp+(p-k)+1]

                self.Qp.append(r)
                self.updateGP(s,(kp,kp+(p-k)),r)
                self.updateGP(r,(kp+(p-k)+1,pp),sp)

                return (False,r)
        else:
            # s is explicit
            if self.existsTransition(s,t):
                return (True,s)
            else:
                return (False,s)


    def canonize(self,s,(k,p)):
        # Given a reference pair (s,(k,p)) for some state r, it finds and returns state s' and left link k'
        # such that (s', (k', p)) is the canonical reference pair for r.
        # State s' is the closest explicit ancestor of r (or r itself if r is explicit).
        # Therefore the string that leads from s' to r must be a suffix of the string t_k...t_p that leads from s to r.
        # Hence the right link p does not change but the left link k can become k' s.t. k' > k.
        if p < k:
            # s already explicit
            return (s,k)
        else:
            ((kp,pp),sp) = self.getTransition(s,self.T[k])

            while pp - kp <= p - k:
                # Move on closer to r
                k = k + (pp - kp) + 1
                s = sp
                if k <= p:
                    ((kp,pp),sp) = self.getTransition(s,self.T[k])

            return (s,k)


    def printST(self):
        print "Suffix Tree for '" + self.T + "'"
        print "Q': " + str(self.Qp)
        print "root: " + str(self.root)
        print "g':"
        pprint(self.gp)
        print "f':"
        pprint(self.fp)




if __name__ == "__main__":
    T = raw_input("Inserisci il testo T: ")
    ST = SuffixTree(T)
    ST.printST()
