def split_labels(label_reader,
                 training_label_writer,
                 testing_label_writer,
                 training_fraction,
                 max_labels=0):
    """Splits a full label set into a training and testing set.

    Given a full set of labels and associated inputs, splits up the labels
    into training and testing sets in the proportion defined by
    training_fraction.

    Args:
        label_reader: A labelled_data.Reader instance that reads the full set
            of labels.
        training_label_writer: A labelled_data.Writer instance that writes out
            the subset of labels to be used for training.
        testing_label_writer: A labelled_data.Writer instance that writes out
            the subset of labels to be used for testing.
        training_fraction: A value between 0.0 and 1.0 that specifies the
            proportion of labels to use for training. Any label not used for
            training is used for testing until max_labels is reached.
        max_labels: The maximum number of labels to read from label_reader. 0
            is treated as infinite.

    """
    labels = _read_labels(label_reader, max_labels)
    _write_labels(labels, training_label_writer, testing_label_writer,
                  training_fraction)


def _read_labels(reader, max_labels):
    labels = []
    for i, label in enumerate(reader):
        if max_labels and i >= max_labels:
            break
        labels.append(label)
    return labels


def _write_labels(labels, training_label_writer, testing_label_writer,
                  training_fraction):
    training_label_count = int(len(labels) * training_fraction)
    training_label_writer.writerows(labels[:training_label_count])
    testing_label_writer.writerows(labels[training_label_count:])
