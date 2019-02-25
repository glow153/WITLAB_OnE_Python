class JFilter:
    def getLimitRange(self, dataArr):
        # find idx of minimum value of left and right side
        mid = int(len(dataArr) / 2)
        leftmin = min(dataArr[:mid])
        rightmin = min(dataArr[mid:])
        leftidx = 0
        rightidx = 0

        for i in range(mid):
            if dataArr[i] == leftmin:
                leftidx = i
                break

        for i in range(mid, len(dataArr)):
            if dataArr[i] == rightmin:
                rightidx = i
                break

        return [leftidx, rightidx]

    def makeNoise(self, srcDataArr):
        import random
        dataArr = list(srcDataArr)
        leftlimidx, rightlimidx = self.getLimitRange(dataArr)
        noiseCount = random.randrange(50, 150)  # between 50 and 99

        for i in range(noiseCount):
            # select data idx randomly
            randIdx = random.randrange(leftlimidx, rightlimidx)
            # add noise on src value randomly
            dataArr[randIdx] += (random.randrange(1000) + random.random())

        return dataArr

    def noiseSelecting(self, dataArr):
        noiseList = []
        section = []
        criteria = 100
        isNoise = False

        leftidx, rightidx = self.getLimitRange(dataArr)

        # detect noise (need to improve performance)
        for i in range(leftidx, rightidx - 5):
            # detect start point of noise section
            if dataArr[i + 1] - dataArr[i] > criteria or \
                    dataArr[i + 2] - dataArr[i] > criteria or \
                    dataArr[i + 3] - dataArr[i] > criteria:
                isNoise = True

            # detect end point of noise section
            elif dataArr[i] - dataArr[i + 1] > criteria:
                isNoise = False

            # check noise data index
            if isNoise:
                section.append(i)
            elif not isNoise and len(section) > 0:
                section.append(i)
                noiseList.append([min(section), max(section) + 1])
                section = []

        return noiseList

    def interpolation(self, srcDataArr, noiseList):
        dataArr = list(srcDataArr)
        # noise value deletion
        for sect in noiseList:
            x0 = sect[0]
            x1 = sect[1]
            y0 = dataArr[x0]
            y1 = dataArr[x1]

            # linear interpolation
            # spline interpolation would be better
            for x in range(sect[0] + 1, sect[1]):
                dataArr[x] = dataArr[x0] + ((y1 - y0) / (x1 - x0)) * (x - x0)

        return dataArr
