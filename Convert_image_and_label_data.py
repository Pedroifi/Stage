# https://www.programmersought.com/article/4120403589/
# https://www.programmersought.com/article/30704348665/
# https://www.programmersought.com/article/85815745002/
# https://www.programmersought.com/article/75492263225/
# https://www.programmersought.com/article/30704348665/

# -*- coding=utf-8 -*-
import tensorflow as tf
import os

Os.environ["TF_CPP_MIN_LOG_LEVEL"] = '2' #Show only warning and Error   

FLAGS = tf.app.flags.FLAGS
 tf.app.flags.DEFINE_string("tfrecords_dir", "./data/captcha.tfrecords", "Verification Code tfrecords File")
 tf.app.flags.DEFINE_string("captcha_dir", "../data/Genpics/", "Captcha Image Path")
 tf.app.flags.DEFINE_string("letter", "ABCDEFGHIJKLMNOPQRSTUVWXYZ", "Type of Captcha Character")


def get_captcha_image(captcha_dir):
    """
         Get captcha image data
         :param captcha_dir: captcha image path
    :return: image
    """
         # Construct file name
    filename = []

    for i in range(6000):
        string = str(i) + ".jpg"
        filename.append(string)

         # Construct path + file
    # file_list = [os.path.join(FLAGS.captcha_dir, file) for file in filename]
    file_list = [os.path.join(captcha_dir, file) for file in filename]

         # Construct file queue
    file_queue = tf.train.string_input_producer(file_list, shuffle=False)

         # 
    reader = tf.WholeFileReader()

         # Read image data content
    key, value = reader.read(file_queue)

         # decode image data
    image = tf.image.decode_jpeg(value)
    image.set_shape([20, 80, 3])

         # Batch processing data [6000, 20, 80, 3]
    image_batch = tf.train.batch([image], batch_size=6000, num_threads=1, capacity=6000)

    return image_batch


def get_captcha_label(captcha_dir):
    """
         Read captcha image tag data
         :param captcha_dir: captcha label path
    :return: label
    """
         # Construct tag data file path
    captcha_dir = captcha_dir + "labels.csv"

         # Construct file queue
    file_queue = tf.train.string_input_producer([captcha_dir], shuffle=False)

         # 
    reader = tf.TextLineReader()

         # Read the label data content of excel
    key, value = reader.read(file_queue)

         # decode csv data
         # records: Specify matrix format and data type
         The 1 in #[1] is used to specify the data type. For example, if there is a decimal in the matrix, it is float, and [1] should be changed to [1.0].
    records = [[1], ["None"]]
    number, label = tf.decode_csv(value, record_defaults=records)

         # Batch data
    label_batch = tf.train.batch([label], batch_size=6000, num_threads=1, capacity=6000)

    return label_batch


def dealwuthlabel(label_str):
    """

    :param label_str:
    :return:
    """
         # Type of verification code string
    letter = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

         #Build character index {0:'A', 1:'B', ...}
    num_letter = dict(enumerate(list(letter)))

         # value pair inversion {'A':0, 'B':1, ...}
    letter_num = dict(zip(num_letter.values(), num_letter.keys()))

    print(letter_num)

         #Build tags to the list
    array = []

         #Processing tag data [[b'NZPP'], ...]
    for string in label_str:
        letter_list = []  # [1, 2, 3, 4]

                 # Modify the encoding, b'NZPP' to the string, and loop to find the number corresponding to the character of each verification code
        for letter in string.decode("utf-8"):
            letter_list.append(letter_num[letter])

        array.append(letter_list)

    # [[13, 25, 15, 15], [22, 10, 7, 10], [22, 15, 18, 9], ...]
    # print(array)

         # Convert array to Tensor type
    label = tf.constant(array)

    return label


def write_to_tfrecords(image_batch, label_batch):
    """
         Write image content and tags to the tfrecords file
         :param image_batch: eigenvalue
         :param label_batch: tag value
    :return: None
    """
         # Conversion type
    label_batch = tf.cast(label_batch, tf.uint8)

    print(label_batch)

         #Create TFRecords memory
    # writer = tf.python_io.TFRecordWriter(path=FLAGS.tfrecords_dir)
    writer = tf.python_io.TFRecordWriter(path="./data/captcha.tfrecords")

         #  Each image data is constructed with the example protocol fast, serialized and written
    for i in range(label_batch.shape[0]):
                 # Take the i-th picture data and convert it to the corresponding type. The eigenvalue of the picture should be converted to a string form.
        image_string = image_batch[i].eval().tostring()

                 #  , converted to integer
        label_string = label_batch[i].eval().tostring()

                 # Constructing a protocol block
        example = tf.train.Example(features=tf.train.Features(feature={
            "image": tf.train.Feature(bytes_list=tf.train.BytesList(value=[image_string])),
            "label": tf.train.Feature(bytes_list=tf.train.BytesList(value=[label_string])),
        }))

        writer.write(example.SerializeToString())

         # Close file
    writer.close()

    return None


if __name__ == '__main__':
         # 
    captcha_dir = "../data/GenPics/"

         #Get the image in the verification code file
    image_batch = get_captcha_image(captcha_dir)

         # Get the tag data in the verification code file
    label = get_captcha_label(captcha_dir)

    print(image_batch, label)

    with tf.Session() as sess:
        coord = tf.train.Coordinator()
        threads = tf.train.start_queue_runners(sess=sess, coord=coord)

        # [b'NZPP' b'WKHK' b'WPSJ' ... b'FVQJ' b'BQYA' b'BCHR']
        label_str = sess.run(label)
        print(label_str)

                 # string tags Convert to digital tensors
        label_batch = dealwuthlabel(label_str)

                 # Write image data and content to the tfrecords file
        write_to_tfrecords(image_batch, label_batch)

        coord.request_stop()
        coord.join(threads)

