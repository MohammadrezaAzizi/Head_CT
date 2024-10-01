def retrieve_images(img_dirlist:list, train_seq, val_seq, test_seq, format:str, color_mode:str, target_size):
  headers = []
  for img_dir in img_dirlist:
    for idx, filename in enumerate(os.listdir(img_dir)):
      if idx<1:
        # /content/drive/MyDrive/P.1/images/JAHANGIRI, MAHBOOBEH_100.jpg
        patient_name = filename.split("_")[0]
        headers.append(patient_name)
      else:
        break
  # Retrieval on train sequences
  for seq in train_seq:
    for ix, img_name in enumerate(seq):
      name = img_name.split("_")[0]
      for idx, header in headers:
        if name == header:
          if type == "tf_obj":
            img_name = tf.keras.utils.load_img(path = str(img_dirlist[0]+img_name),
                                               color_mode= color_mode, target_size= target_size)
            # To see if this works already without reassigning on the seq list
            #print(seq)
            seq[ix] = img_name

# Retrieval on validation sequences
  for seq in val_seq:
    for ix, img_name in enumerate(seq):
      name = img_name.split("_")[0]
      for idx, header in headers:
        if name == header:
          if type == "tf_obj":
            img_name = tf.keras.utils.load_img(path = str(img_dirlist[0]+img_name),
                                               color_mode= color_mode, target_size= target_size)
            seq[ix] = img_name

# Retrieval on test sequences
  for seq in test_seq:
    for ix, img_name in enumerate(seq):
      name = img_name.split("_")[0]
      for idx, header in headers:
        if name == header:
          if type == "tf_obj":
            img_name = tf.keras.utils.load_img(path = str(img_dirlist[0]+img_name),
                                               color_mode= color_mode, target_size= target_size)
            seq[ix] = img_name

  return train_seq, val_seq, test_seq