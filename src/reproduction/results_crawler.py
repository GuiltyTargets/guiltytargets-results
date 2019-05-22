import os

import pandas as pd
from constants import data_dir, mappings, output_file_path


def get_folders(parent_dir):
    contents = os.listdir(parent_dir)
    for name in contents:
        path = os.path.join(parent_dir, name)
        if not os.path.isfile(path) and name != "old":
            yield path


def write_to_file(output_file, line_beginning, method, auc_values):
    for auc in auc_values:
        print("{},{},{}".format(line_beginning, method, auc), file=output_file)


def main():
    with open(output_file_path, mode="w") as output_file:
        print("{},{},{},{},{},{},{}".format("Dataset",
                                            "PPI Network",
                                            "Target DB",
                                            "LFC Cutoff",
                                            "Confidence Cutoff",
                                            "Method",
                                            "AUC"),
              file=output_file)
        for folder in get_folders(data_dir):
            for result_folder in get_folders(folder):
                parent_folder_path, folder_name = os.path.split(result_folder)
                _, dataset = os.path.split(parent_folder_path)

                try:
                    _, graph, dtdb, merge = folder_name.split("-")
                    lfc_cutoff, conf_cutoff = merge[0:3], merge[3:]

                    line_beginning = "{},{},{},{},{}".format(
                        dataset,
                        mappings[graph],
                        mappings[dtdb],
                        lfc_cutoff,
                        conf_cutoff
                    )
                    try:
                        gat2vec_auc_path = os.path.join(result_folder, "auc.tsv")
                        gat2vec_aucs = pd.read_csv(gat2vec_auc_path, sep="\t")["auc"].values.tolist()

                        write_to_file(output_file, line_beginning, "GuiltyTargets", gat2vec_aucs)
                    except:
                        print("No GuiltyTargets results in: ", result_folder)
                except:
                    print("Not a proper file name     : ", result_folder)



if __name__ == '__main__':
    main()
