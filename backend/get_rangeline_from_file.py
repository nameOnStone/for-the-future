from tsv2json.core import TSV


def main(path_of_file, start=0, end=10):
    '''path_of_file must be tsv file'''

    mem = []
    for ls in TSV(path_of_file).data:
        mem.append(ls)

    return {"trunk_data": mem[start: end], "dataCount": len(mem)}


if __name__ == "__main__":
    print(main("dbSamples/PN220258_D.normal.filtered.vep.filtered.maf", start=0, end=10))
    #print(get_trunck_file("dbSamples/97H-0110.featurecount.gene_id.tpm.txt", start=10, end=20))
