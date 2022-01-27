# featureExtractors.py
# --------------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"Feature extractors for Pacman game states"

from game import Directions, Actions
from pacman import SCARED_TIME
import util

class FeatureExtractor:
    def getFeatures(self, state, action):
        """
          Returns a dict from features to counts
          Usually, the count will just be 1.0 for
          indicator functions.
        """
        util.raiseNotDefined()

class IdentityExtractor(FeatureExtractor):
    def getFeatures(self, state, action):
        feats = util.Counter()
        feats[(state,action)] = 1.0
        return feats

class CoordinateExtractor(FeatureExtractor):
    def getFeatures(self, state, action):
        feats = util.Counter()
        feats[state] = 1.0
        feats['x=%d' % state[0]] = 1.0
        feats['y=%d' % state[0]] = 1.0
        feats['action=%s' % action] = 1.0
        return feats

def closestFood(pos, food, walls):
    """
    closestFood -- this is similar to the function that we have
    worked on in the search project; here its all in one place
    """
    fringe = [(pos[0], pos[1], 0)]
    expanded = set()
    while fringe:
        pos_x, pos_y, dist = fringe.pop(0)
        if (pos_x, pos_y) in expanded:
            continue
        expanded.add((pos_x, pos_y))
        # if we find a food at this location then exit
        if food[pos_x][pos_y]:
            return dist
        # otherwise spread out from the location to its neighbours
        nbrs = Actions.getLegalNeighbors((pos_x, pos_y), walls)
        for nbr_x, nbr_y in nbrs:
            fringe.append((nbr_x, nbr_y, dist+1))
    # no food found
    return None

class SimpleExtractor(FeatureExtractor):
    """
    Returns simple features for a basic reflex Pacman:
    - whether food will be eaten
    - how far away the next food is
    - whether a ghost collision is imminent
    - whether a ghost is one step away
    """

    def getFeatures(self, state, action):
        # extract the grid of food and wall locations and get the ghost locations
        food = state.getFood()
        walls = state.getWalls()
        ghosts = state.getGhostPositions()

        features = util.Counter()

        features["bias"] = 1.0

        # compute the location of pacman after he takes the action
        x, y = state.getPacmanPosition()
        dx, dy = Actions.directionToVector(action)
        next_x, next_y = int(x + dx), int(y + dy)

        # count the number of ghosts 1-step away
        features["#-of-ghosts-1-step-away"] = sum((next_x, next_y) in Actions.getLegalNeighbors(g, walls) for g in ghosts)

        # if there is no danger of ghosts then add the food feature
        if not features["#-of-ghosts-1-step-away"] and food[next_x][next_y]:
            features["eats-food"] = 1.0

        dist = closestFood((next_x, next_y), food, walls)
        if dist is not None:
            # make the distance a number less than one otherwise the update
            # will diverge wildly
            features["closest-food"] = float(dist) / (walls.width * walls.height)
        features.divideAll(10.0)
        return features

class NewExtractor(FeatureExtractor):
   
    def closestTarget(self, pos, objects, walls):
        if not objects:
            return None

        fringe = [(pos[0], pos[1], 0)]
        expanded = set()
        while fringe:
            pos_x, pos_y, dist = fringe.pop(0)
            if (pos_x, pos_y) in expanded:
                continue
            expanded.add((pos_x, pos_y))
            # if we find a object at this location then exit
            if (pos_x, pos_y) in objects:
                return dist
            # otherwise spread out from the location to its neighbours
            nbrs = Actions.getLegalNeighbors((pos_x, pos_y), walls)
            for nbr_x, nbr_y in nbrs:
                fringe.append((nbr_x, nbr_y, dist+1))
        # no object found
        return None
    
    def getNextGhostPos(self, ghostState):
        x, y = ghostState.getPosition()
        dx, dy = Actions.directionToVector(ghostState.getDirection())
        return (int(x + dx), int(y + dy))

    def closestGhost(self, pos, ghostState, walls):
        ghost = self.getNextGhostPos(ghostState)
        
        fringe = [(pos[0], pos[1], 0)]
        expanded = set()
        while fringe:
            pos_x, pos_y, dist = fringe.pop(0)
            if (pos_x, pos_y) in expanded:
                continue
            expanded.add((pos_x, pos_y))
            # If we find a ghost at this location then exit
            if ghost == (pos_x, pos_y):
                # make the distance a number less than one otherwise the update
                # will diverge wildly
                return float(dist) / (walls.width * walls.height)
            # Otherwise spread out from the location to its neighbours
            nbrs = Actions.getLegalNeighbors((pos_x, pos_y), walls)
            for nbr_x, nbr_y in nbrs:
                fringe.append((nbr_x, nbr_y, dist+1))
        # no ghost found
        return None

    def checkForSafePath(self, pacmanPos, ghostPos, walls):
        pacFringe = 1
        fringe = []

        # no active ghosts around
        if len(ghostPos) == 0:
            return True

        # append the ghosts to fringe
        # format: identity, ghost_position, dist
        for ghost in ghostPos:
            fringe.append(('ghost', ghost, 0))

        # BFS to find ghosts 2 steps away
        ghostExpanded = set()
        ghostHeadStart = 2 # we are interested in ghosts that are 2 steps away
        while len(fringe) > 0:
            identity, pos, dist = fringe.pop(0)
            if pos in ghostExpanded:
                continue
            if dist >= ghostHeadStart:
                fringe.append((identity, pos, dist))
                break
            ghostExpanded.add(pos)
            # otherwise spread out from the location to its neighbours
            nbrs = Actions.getLegalNeighbors(pos, walls)
            for nbr_x, nbr_y in nbrs:
                fringe.append(('ghost', (nbr_x, nbr_y), dist+1))
            
        # append pacman to fringe
        # format: identity, pacman_position, dist
        fringe.append(('pacman', pacmanPos, 0))
        expanded = set()

        # BFS to check whether is there safe path for pacman
        while pacFringe > 0:
            identity, pos, dist = fringe.pop(0)
            if identity is 'pacman':
                pacFringe -= 1
                expanded.add(pos)
                nbrs = Actions.getLegalNeighbors(pos, walls)
                # to check whether there are safe neighbour positions
                safePos = [nb for nb in nbrs if nb not in expanded and nb not in ghostExpanded]
                # if there is a split path or no more path, stop exploring
                if len(safePos) > 1:
                    return True
                elif len(safePos) == 1:
                    # still cannot decide properly
                    pacFringe += 1
                    fringe.append(('pacman', safePos[0], dist + 1))
                else:
                    return False
            else:
                if pos in ghostExpanded:
                    continue
                ghostExpanded.add(pos)
                # otherwise spread out from the location to its neighbours
                nbrs = Actions.getLegalNeighbors(pos, walls)
                for nbr_x, nbr_y in nbrs:
                    fringe.append(('ghost', (nbr_x, nbr_y), dist+1))
        # no safe path
        return False
    

    """
    Generate your own feature
    """
    def getFeatures(self, state, action):
        # extract the grid of food and wall locations and get the ghost locations
        food = state.getFood()
        walls = state.getWalls()
        ghostStates = state.getGhostStates()
        
        # extract capsules positions
        capsules = state.getCapsules()
        
        # to store ghosts that can kill
        activeGhostPositions = []
        
        # to store scared ghosts
        unactiveGhostPositions = []
        unActiveGhost = []
        hasUnactiveGhost = False

        for ghost in ghostStates:
            if ghost.scaredTimer <= 1:
                activeGhostPositions.append(ghost.getPosition())
            if ghost.scaredTimer > 1:
                unactiveGhostPositions.append(ghost.getPosition())
                unActiveGhost.append(ghost)
                hasUnactiveGhost = True
        
        features = util.Counter()
        features["bias"] = 1.0

        # compute the location of pacman after he takes the action
        x, y = state.getPacmanPosition()
        dx, dy = Actions.directionToVector(action)
        next_x, next_y = int(x + dx), int(y + dy)
        nextPos = (next_x, next_y)

        # compute whether a safe path exist
        numpaths = self.checkForSafePath((next_x, next_y), activeGhostPositions, walls)
        if numpaths is False:
            features["no-safe-route"] = 1.0

        # notTrap = True
        # for g in unActiveGhost:
        #     if nextPos == g.getPosition() and nextPos in activeGhostPositions:
        #         notTrap = False
        #         print ("trapped")
        #         break
        
        # check if ghost in next position
        notTrap = True
        if nextPos in activeGhostPositions:
            features["ghost-in-next-position"] = 1.0
            notTrap = False

        # compute closest scared ghost
        allClosestScaredGhostStates = []       
        for ghostState in unActiveGhost:
            if self.closestGhost((next_x, next_y), ghostState, walls) is not None:
                allClosestScaredGhostStates.append(ghostState)

     
        if allClosestScaredGhostStates:
            closestGhostState = min(
                allClosestScaredGhostStates,
                key=lambda ghostState: self.closestGhost((next_x, next_y), ghostState, walls))
            
            # finding dist between closest scared ghost respawn and pacman next position
            pacmanRespawnDist = self.closestTarget(closestGhostState.start.getPosition(), (nextPos, ), walls)
            # finding dist between closest scared ghost and its respawn position
            ghostRespawnDist = self.closestTarget(closestGhostState.start.getPosition(), (closestGhostState.getPosition(), ), walls)
            
            # if (pacmanRespawnDist > 0 and (ghostRespawnDist > 1 or pacmanRespawnDist > 1)):
            if ((ghostRespawnDist > 0 and (ghostRespawnDist > 1 or pacmanRespawnDist > 1)) \
                or (pacmanRespawnDist > 0 and (ghostRespawnDist > 1 or pacmanRespawnDist > 1))):
                # if scared ghost at next position, priortise eating the ghost 
                if nextPos in unactiveGhostPositions:
                    features["eats-scared-ghost"] = 1.0
                # eat scared ghost if safe path exist
                features['closest-scared-ghost-distance'] = 1 - self.closestGhost((next_x, next_y), closestGhostState, walls)
                
        # find active ghosts around
        features['#-of-strong-ghost-1-step-away'] = sum(
            (next_x, next_y) in Actions.getLegalNeighbors(ghostState, walls) 
            for ghostState in activeGhostPositions)
        
        hasActiveGhostNeighbor = False
        if features['#-of-strong-ghost-1-step-away'] != 0:
            hasActiveGhostNeighbor = True

        capsuleDist = self.closestTarget((next_x, next_y), capsules, walls)
        foodDist = closestFood((next_x, next_y), food, walls)

        # if there are no active ghosts around or scared ghosts to eat,
        # eat a capsule 
        if not hasUnactiveGhost and numpaths is True and not hasActiveGhostNeighbor and (next_x, next_y) in capsules:
            features['eat-capsule'] = 1.0
        
        # if there are no active ghosts around or scared ghosts to eat,
        # or no capsules to eat,
        # then, eat food
        if not hasUnactiveGhost and numpaths is True and not hasActiveGhostNeighbor and not capsules and not (next_x, next_y) in capsules and food[next_x][next_y] :
            features['eats-food'] = 1.0
        
        # in other cases, priority for capsule than food
        if not hasUnactiveGhost and capsuleDist is not None:
            features['closest-capsule'] = float(capsuleDist) / (walls.width * walls.height)
        if not hasUnactiveGhost and not capsules and foodDist is not None:
            # make the distance a number less than one otherwise the update
            # will diverge wildly
            features['closest-food'] = float(foodDist) / (walls.width * walls.height)
   
        features.divideAll(10.0)

        return features
