class NewExtractor(FeatureExtractor):
    """
    Design you own feature extractor here. You may define other helper functions you find necessary.
    """
    """
    Design you own feature extractor here. You may define other helper functions you find necessary.
    """
    
    def nearestPosition(self, start, targets, walls):
        if len(targets) == 0:
            return None
        fringe = [(start[0], start[1], 0)]
        expanded = set()
        while fringe:
            pos_x, pos_y, dist = fringe.pop(0)
            if (pos_x, pos_y) in expanded:
                continue
            expanded.add((pos_x, pos_y))
            # if we find a target at this location then exit
            if (pos_x, pos_y) in targets:
                return dist
            # otherwise spread out from the location to its neighbours
            nbrs = Actions.getLegalNeighbors((pos_x, pos_y), walls)
            for nbr_x, nbr_y in nbrs:
                fringe.append((nbr_x, nbr_y, dist+1))
        # no target found
        return None
    
    def analyseSafePaths(self, pacmanPos, dangerousGhostPositions, walls):
        if len(dangerousGhostPositions) == 0:
            return 2
        
        pacmanFringeCount = 1
        numOfSafeRoutes = 0
        fringe = []
        
        for ghost in dangerousGhostPositions:
            fringe.append((ghost, 0, 'ghost'))

        ghostExpanded = set()
        ghostHeadStart = 2
        while len(fringe) > 0:
            pos, dist, identity = fringe.pop(0)
            if pos in ghostExpanded:
                continue
            if dist >= ghostHeadStart:
                fringe.append((pos, dist, identity))
                break
            ghostExpanded.add(pos)
            ghostNeighbors = Actions.getLegalNeighbors(pos, walls)
            for neighbor in ghostNeighbors:
                fringe.append((neighbor, dist + 1, 'ghost'))

        fringe.append((pacmanPos, 0, 'pacman'))
        expanded = set()

        while pacmanFringeCount > 0:
            pos, dist, identity = fringe.pop(0)
            if identity is 'pacman':
                pacmanFringeCount -= 1

                expanded.add(pos)
                pacmanNeighbors = Actions.getLegalNeighbors(pos, walls)
                nextPositions = [a for a in pacmanNeighbors if a not in ghostExpanded and a not in expanded]
                # if there is a split path or no more path, stop exploring
                if len(nextPositions) != 1:
                    if len(nextPositions) > 1:
                        numOfSafeRoutes += 1
    
                    continue
                else:
                    pacmanFringeCount += 1
                    fringe.append((nextPositions[0], dist + 1, 'pacman'))
            else:
                if pos in ghostExpanded:
                    continue
                ghostExpanded.add(pos)
                ghostNeighbors = Actions.getLegalNeighbors(pos, walls)
                for neighbor in ghostNeighbors:
                    fringe.append((neighbor, dist + 1, 'ghost'))

        return numOfSafeRoutes

    def getWeakGhostStates(self, ghostStates):
        return list(filter(lambda ghostState: ghostState.scaredTimer > 0, ghostStates))

    def getFeatures(self, state, action):
        "*** YOUR CODE HERE ***"
        # extract the grid of food and wall locations and get the ghost locations
        food = state.getFood()
        walls = state.getWalls()
        ghostStates = state.getGhostStates()
        capsules = state.getCapsules()
        capsuleList = list(capsules)
        #dangerousGhostPositions = list((g.getPosition() for g in ghostStates if g.scaredTimer <= 1))
        #safeGhostPositions = list((g.getPosition() for g in ghostStates if g.scaredTimer > 0))

        dangerousGhostPositions = []
        safeGhostPositions = []

        for ghost in ghostStates:
            if ghost.scaredTimer <= 1:
                dangerousGhostPositions.append(ghost.getPosition())
            if ghost.scaredTimer > 0:
                safeGhostPositions.append(ghost.getPosition())

        features = util.Counter()

        features["bias"] = 1.0

        # compute the location of pacman after he takes the action
        x, y = state.getPacmanPosition()
        dx, dy = Actions.directionToVector(action)
        next_x, next_y = int(x + dx), int(y + dy)
        next_pos = (next_x, next_y)

        dist = closestFood(next_pos, food, walls)
        if dist is not None:
            features["closest-food"] = float(dist) / (walls.width * walls.height)

        # check if next_pos has dangerous ghost
        if next_pos in dangerousGhostPositions:
            features["ghosts-in-next-pos"] = 1.0

        numSafeRoutes = 4

        # count number of safe paths
        if len(Actions.getLegalNeighbors(next_pos, walls)) <= 3:
            numSafeRoutes = self.analyseSafePaths(next_pos, dangerousGhostPositions, walls)
            #print (numSafeRoutes)
            if numSafeRoutes == 0:
                features["trapped"] = 1.0

        # count the number of ghosts 1-step away that dangerous
        features["#-of-ghosts-1-step-away"] = sum( next_pos in Actions.getLegalNeighbors(g, walls) for g in dangerousGhostPositions)
        

        weakGhostStates = list(filter(
            lambda ghostState: distanceGhostState((next_x, next_y), ghostState, walls) is not None,
            self.getWeakGhostStates(ghostStates)
        ))


        

        if weakGhostStates:
            nearestScaredGhost = min(
                weakGhostStates,
                key=lambda ghostState: distanceGhostState((next_x, next_y), ghostState, walls))
            nearestScaredGhostDist = nearestScaredGhost.scaredTimer
            #nearestScaredGhostDist = distanceGhostState((next_x, next_y), nearestScaredGhost, walls)


            if not features["#-of-ghosts-1-step-away"] and numSafeRoutes != 0:
                
                if nearestScaredGhost is not None:
                    pacmanDistFromRespawn = self.nearestPosition(nearestScaredGhost.start.getPosition(), (next_pos, ), walls)
                    ghostDistFromRespawn = self.nearestPosition(nearestScaredGhost.start.getPosition(), (nearestScaredGhost.getPosition(), ), walls)
                    # if pacman or scared ghost are not near respawn location
                    if (ghostDistFromRespawn > 0 or pacmanDistFromRespawn > 0) and (ghostDistFromRespawn > 1 or pacmanDistFromRespawn > 1):
                        features["closest-scared-ghost"] = 1.0 - float(nearestScaredGhostDist) / (walls.width * walls.height)
                        if next_pos in safeGhostPositions:
                            features["eats-ghost"] = 1.0
                   
            
            # if there is no danger of ghosts then add the food feature
            if food[next_x][next_y] and nearestScaredGhost is None:
                features["eats-food"] = 1.0
            
            nearestCapsuleDist = self.nearestPosition(next_pos, capsuleList, walls)
            if nearestCapsuleDist is not None:
                features["closest-capsule"] = 1.0 - float(nearestCapsuleDist) / (walls.width * walls.height)
        
        features.divideAll(10.0)
        return features

