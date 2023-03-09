from random import randint
import numpy as np

normalVoltage = 5.00
conversionFactor = normalVoltage/1023
sampleData = list()

def getRandom(min: int, max: int) -> int:
    return randint(min, max)


def createTestData(min, max, count):
    for _ in range(count):
        newVoltage = getRandom(min, max) * conversi--onFactor
        sampleData.append(newVoltage)


def testData(normalVoltage=5.00):
    average = 0
    deviation = 0
    average2 = 0
    for i, data in enumerate(sampleData):
        i += 1
        average = ((average * (i - 1)) + data) / i
        deviation = ((deviation * (i - 1)) + (normalVoltage - data)) / i
        average2 += data
    deviation = round((deviation / normalVoltage) * 100, 3)
    print(f"\n-----Completed Values-----\nCalculated Average: {average:.3f}\nAverage Deviation:"
          f"{deviation}%\nNumpy Average: {np.average(sampleData):.3f}\n"
          f"Traditional Average: {average2 / len(sampleData):.3f}")


createTestData(1023, 1023, 500)
testData()
