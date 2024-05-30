class partialdataIO:
    def savepartialdata(path, partial_data, instruction_tag):
        output_file_instructiontag = open (path + '/instruction_tag.txt', "w")
        for item in instruction_tag:
            output_file_instructiontag.write(str(item) + '\n')
        output_file_instructiontag.close()
        for i in range(0, len(instruction_tag)):
            output_file_partialdata = open (path + '/partialdata_' + str(i), "wb")
            output_file_partialdata.write(partial_data[i])
            output_file_partialdata.close()