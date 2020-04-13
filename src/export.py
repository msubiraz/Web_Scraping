
class export_csv():

    def __init__(self, filename):
        # Overwrite to the specified file.
		# Create it if it does not exist.
        file = open("../csv/" + filename, "w+")

		# Dump all the data with CSV format
        for i in range(len(self.data)):
            for j in range(len(self.data[i])):
                file.write(self.data[i][j] + ";");
            file.write("\n");


with open(filePath, 'w', newline='') as csvFile:
  writer = csv.writer(csvFile)
  for priceElement in priceList:
    writer.writerow(priceElement)



        