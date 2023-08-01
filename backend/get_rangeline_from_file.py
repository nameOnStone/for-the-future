from tsv2json.core import TSV


def main(path_of_file, start=0, end=10):
    '''path_of_file must be tsv file'''

    mem = []
    for ls in TSV(path_of_file).data:
        mem.append(ls)

    return {"trunk_data": mem[start: end], "dataCount": len(mem)}


if __name__ == "__main__":
    pass
