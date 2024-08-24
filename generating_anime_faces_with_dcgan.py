{"metadata":{"kernelspec":{"language":"python","display_name":"Python 3","name":"python3"},"language_info":{"name":"python","version":"3.10.12","mimetype":"text/x-python","codemirror_mode":{"name":"ipython","version":3},"pygments_lexer":"ipython3","nbconvert_exporter":"python","file_extension":".py"},"kaggle":{"accelerator":"nvidiaTeslaT4","dataSources":[{"sourceId":737475,"sourceType":"datasetVersion","datasetId":379764}],"dockerImageVersionId":30528,"isInternetEnabled":true,"language":"python","sourceType":"script","isGpuEnabled":true}},"nbformat_minor":4,"nbformat":4,"cells":[{"cell_type":"code","source":"# %% [markdown]\n# # <p><center style=\"font-family:newtimeroman;font-size:180%;\"> Generating Anime Faces with DCGAN: A Dataset of High-Quality Anime </center></p>\n# ### Table of contents:\n# \n# * [Introduction](#1)\n# * [Import Libraries](#2)\n# * [Import DataSet](#3)\n# * [Preprocessing](#4)\n# * [Create Generator](#5)\n# * [Create Discriminator](#6)\n# * [Create Deep Convolutional GAN](#7)\n# * [Train The Model](#8)\n# * [Evaluation Of Model Results](#9)\n\n# %% [markdown] {\"execution\":{\"iopub.status.busy\":\"2023-08-14T19:17:39.966306Z\",\"iopub.execute_input\":\"2023-08-14T19:17:39.967019Z\"}}\n# <a id=\"1\"></a>\n# # <p style=\"background-image: url(https://i.postimg.cc/K87ByXmr/stage5.jpg);font-family:camtasia;font-size:120%;color:white;text-align:center;border-radius:15px 50px; padding:7px\"> Introduction </p>\n\n# %% [markdown]\n# <html>\n# <body>\n#   <h1>Generating Anime Faces with DCGAN: A Dataset of High-Quality Anime Girls</h1>\n#   <p> In this project, we aim to generate high-quality anime faces using the Deep Convolutional Generative Adversarial Networks (DCGAN) algorithm. The dataset used for this project consists of 63,632 anime faces, carefully curated to ensure quality and appeal.\n# The motivation behind this project is to fulfill the simple dream of generating perfect waifus, cute female anime faces that capture the essence of the anime art style. \n# The DCGAN algorithm offers an attractive approach to generating realistic and visually appealing anime faces. By training the generator and discriminator networks in an adversarial learning process, we can learn a hierarchy of representations, starting from object parts and progressing to scenes. This allows us to create compelling and diverse anime face images.\n# To showcase the capabilities of the project, we provide examples of both real and generated anime face images. By comparing the \"real vs. fake\" images, viewers can appreciate the quality and realism achieved through the DCGAN algorithm.\n# By combining the power of DCGAN and a meticulously curated anime face dataset, we aim to contribute to the world of anime art and provide a valuable resource for researchers, artists, and fans alike. Join us on this exciting journey to generate captivating anime faces and bring your favorite characters to life!</p>\n# </body>\n# </html>\n\n# %% [markdown]\n# <a id=\"2\"></a>\n# # <p style=\"background-image: url(https://i.postimg.cc/K87ByXmr/stage5.jpg);font-family:camtasia;font-size:120%;color:white;text-align:center;border-radius:15px 50px; padding:7px\">Import Libraries </p>\n\n# %% [code] {\"execution\":{\"iopub.status.busy\":\"2023-10-17T14:35:53.841338Z\",\"iopub.execute_input\":\"2023-10-17T14:35:53.841995Z\",\"iopub.status.idle\":\"2023-10-17T14:35:56.821462Z\",\"shell.execute_reply.started\":\"2023-10-17T14:35:53.841957Z\",\"shell.execute_reply\":\"2023-10-17T14:35:56.820495Z\"}}\n# import requirement libraries and tools\nfrom tensorflow import keras\nimport numpy as np\nimport tensorflow as tf\nimport matplotlib.pyplot as plt\nimport seaborn as sns\nsns.set(style= \"darkgrid\", color_codes = True)\nfrom tensorflow.keras.models import Sequential\nfrom tensorflow.keras.layers import Conv2D, MaxPooling2D, Dense, Flatten, Conv2DTranspose, Reshape, BatchNormalization, Dropout, Input, ReLU, LeakyReLU\nfrom keras.preprocessing.image import ImageDataGenerator\nfrom tensorflow.keras.optimizers import Adam\nfrom tensorflow.keras.losses import BinaryCrossentropy\nfrom PIL import Image\n\nimport warnings\nwarnings.filterwarnings('ignore')\n\n# %% [code]\n<a id=\"3\"></a>\n# <p style=\"background-image: url(https://i.postimg.cc/K87ByXmr/stage5.jpg);font-family:camtasia;font-size:120%;color:white;text-align:center;border-radius:15px 50px; padding:7px\"> Import DataSet </p>\n<a class=\"btn\" href=\"#home\">Tabel of Contents</a>\n\n# %% [code] {\"execution\":{\"iopub.status.busy\":\"2023-10-17T14:35:56.823402Z\",\"iopub.execute_input\":\"2023-10-17T14:35:56.824269Z\",\"iopub.status.idle\":\"2023-10-17T14:36:26.85088Z\",\"shell.execute_reply.started\":\"2023-10-17T14:35:56.824216Z\",\"shell.execute_reply\":\"2023-10-17T14:36:26.849906Z\"}}\n# Loading and Preparing Anime Face Images Dataset using Keras Image Data Generator\nimg_width, img_height = 256, 256\nbatchsize = 32\n\ntrain = keras. utils.image_dataset_from_directory(\n    directory='/kaggle/input/animefacedataset',\n    batch_size = batchsize,\n    image_size = (img_width, img_height))\n\n# %% [markdown]\n# **<a id=\"4\"></a>\n# # <p style=\"background-image: url(https://i.postimg.cc/K87ByXmr/stage5.jpg);font-family:camtasia;font-size:120%;color:white;text-align:center;border-radius:15px 50px; padding:7px\"> Preprocessing </p>\n# <a class=\"btn\" href=\"#home\">Tabel of Contents</a>\n\n# %% [code] {\"execution\":{\"iopub.status.busy\":\"2023-10-17T17:57:20.47248Z\",\"iopub.execute_input\":\"2023-10-17T17:57:20.472878Z\",\"iopub.status.idle\":\"2023-10-17T17:57:21.803092Z\",\"shell.execute_reply.started\":\"2023-10-17T17:57:20.472845Z\",\"shell.execute_reply\":\"2023-10-17T17:57:21.802238Z\"}}\n# Visualizing a Batch of Anime Face Images\n\ndata_iterator = train.as_numpy_iterator()\nbatch = data_iterator.next()\nfig, ax = plt.subplots(ncols=4, figsize=(10,10))\nfor idx, img in enumerate(batch[0][:4]):\n    ax[idx].imshow(img.astype(int))\n    ax[idx].title.set_text(batch[1][idx])\n\n# %% [code] {\"execution\":{\"iopub.status.busy\":\"2023-10-17T18:01:29.109196Z\",\"iopub.execute_input\":\"2023-10-17T18:01:29.109589Z\",\"iopub.status.idle\":\"2023-10-17T18:02:05.444212Z\",\"shell.execute_reply.started\":\"2023-10-17T18:01:29.10956Z\",\"shell.execute_reply\":\"2023-10-17T18:02:05.443185Z\"}}\n# Generating Augmented Batches of Anime Face Images using ImageDataGenerator\nDIR = '/kaggle/input/animefacedataset' #path\n\n# Create an ImageDataGenerator object with data augmentation options for image preprocessing\ntrain_datagen = ImageDataGenerator(rescale=1./255,\n                                   horizontal_flip = True)\n\ntrain_generator = train_datagen.flow_from_directory(\n        DIR,\n        target_size = (64, 64),\n        batch_size = batchsize,\n        class_mode = None)\n\n#train_generator[0]\n\n# %% [markdown]\n# <html>\n# <head>\n# </head>\n# <body>\n#   <h1>Deep Convolutional Generative Adversarial Network</h1>\n#   <p>DCGAN (Deep Convolutional Generative Adversarial Network) is an advanced architecture and training methodology for generative adversarial networks (GANs) specifically designed for image synthesis tasks. It combines deep convolutional neural networks with the adversarial learning framework to generate high-quality and realistic images. </p>\n# </body>\n# </html>\n\n# %% [markdown]\n# <a id=\"5\"></a>\n# # <p style=\"background-image: url(https://i.postimg.cc/K87ByXmr/stage5.jpg);font-family:camtasia;font-size:120%;color:white;text-align:center;border-radius:15px 50px; padding:7px\"> Create Generator </p>\n# <a class=\"btn\" href=\"#home\">Tabel of Contents</a>\n\n# %% [markdown]\n# <html>\n# <head>\n# </head>\n# <body>\n#   <h1> The Generator </h1>\n#   <p>In DCGAN, the generator and discriminator networks play crucial roles. The generator is responsible for generating synthetic images that resemble the target data distribution. It takes random noise as input and gradually transforms it into higher-dimensional outputs using convolutional layers, transposed convolutions, and activation functions like ReLU. Batch normalization is often used to stabilize the learning process. </p>\n# </body>\n# </html>\n\n# %% [code] {\"execution\":{\"iopub.status.busy\":\"2023-10-17T18:02:05.446646Z\",\"iopub.execute_input\":\"2023-10-17T18:02:05.448029Z\",\"iopub.status.idle\":\"2023-10-17T18:02:05.696917Z\",\"shell.execute_reply.started\":\"2023-10-17T18:02:05.44799Z\",\"shell.execute_reply\":\"2023-10-17T18:02:05.695904Z\"}}\n# Creating the Generator Model \n\nKI = keras.initializers.RandomNormal(mean=0.0, stddev=0.02)\ninput_dim = 300\n\ndef Generator_Model():\n\n    Generator = Sequential()\n\n    # Random noise\n    Generator.add(Dense(8 * 8 * 512, input_dim = input_dim))\n    Generator.add(ReLU())\n    # Convert 1d to 3d\n    Generator.add(Reshape((8, 8, 512)))\n    # Unsample\n    Generator.add(Conv2DTranspose(256, (4, 4), strides=(2, 2), padding='same', kernel_initializer=KI, activation='ReLU'))\n    Generator.add(Conv2DTranspose(128, (4, 4), strides=(2, 2), padding='same', kernel_initializer=KI, activation='ReLU'))\n    Generator.add(Conv2DTranspose(64, (4, 4), strides=(2, 2), padding='same', kernel_initializer=KI, activation='ReLU'))\n    Generator.add(Conv2D(3, (4, 4), padding='same', activation='sigmoid'))\n\n    \n    return Generator\n    \ngenerator = Generator_Model()\ngenerator.summary()\n# Visualized Layers of generator\nkeras.utils.plot_model(generator, show_shapes=True)\n\n# %% [markdown]\n# <a id=\"6\"></a>\n# # <p style=\"background-image: url(https://i.postimg.cc/K87ByXmr/stage5.jpg);font-family:camtasia;font-size:120%;color:white;text-align:center;border-radius:15px 50px; padding:7px\"> Create Discriminator </p>\n# <a class=\"btn\" href=\"#home\">Tabel of Contents</a>\n\n# %% [markdown]\n# <html>\n# <head>\n# </head>\n# <body>\n#   <h1> The Discriminator </h1>\n#   <p> The discriminator, on the other hand, aims to distinguish between real and generated images. It utilizes convolutional layers, activation functions, and strided convolutions to downsample the spatial dimensions and capture image features. The discriminator is trained to maximize its ability to correctly classify images as real or fake. </p>\n# </body>\n# </html>\n\n# %% [code] {\"execution\":{\"iopub.status.busy\":\"2023-10-17T18:02:05.698508Z\",\"iopub.execute_input\":\"2023-10-17T18:02:05.699133Z\",\"iopub.status.idle\":\"2023-10-17T18:02:05.982782Z\",\"shell.execute_reply.started\":\"2023-10-17T18:02:05.699089Z\",\"shell.execute_reply\":\"2023-10-17T18:02:05.981889Z\"}}\n# Creating the discriminator Model \n\ndef Discriminator_Model():\n    input_shape = (64, 64, 3)\n\n    # Create a Sequential model\n    discriminator = Sequential()\n    discriminator.add(Conv2D(64,kernel_size=(3, 3), activation='LeakyReLU', input_shape = input_shape))\n    discriminator.add(MaxPooling2D(pool_size=(2, 2)))\n    discriminator.add(Conv2D(128, kernel_size=(3, 3), activation='LeakyReLU'))\n    discriminator.add(MaxPooling2D(pool_size=(2, 2)))\n    discriminator.add(Conv2D(256, kernel_size=(3, 3), activation='LeakyReLU'))\n    discriminator.add(MaxPooling2D(pool_size=(2, 2)))\n    discriminator.add(Flatten())\n    discriminator.add(Dense(256, activation='LeakyReLU'))\n    discriminator.add(Dense(1, activation='sigmoid'))\n\n    return discriminator\n\n# Training The CNN\ndiscriminator = Discriminator_Model()\ndiscriminator.summary()  \n# Visualized Layers of discriminator\nkeras.utils.plot_model(discriminator, show_shapes=True)\n\n# %% [markdown]\n# <a id=\"7\"></a>\n# # <p style=\"background-image: url(https://i.postimg.cc/K87ByXmr/stage5.jpg);font-family:camtasia;font-size:120%;color:white;text-align:center;border-radius:15px 50px; padding:7px\"> Create Deep Convolutional GAN </p>\n# <a class=\"btn\" href=\"#home\">Tabel of Contents</a>\n\n# %% [markdown]\n# <html>\n# <head>\n# </head>\n# <body>\n#   <h1> The Training Process </h1>\n#   <p> The training process of DCGAN involves an adversarial interplay between the generator and discriminator. The generator aims to generate increasingly realistic images to deceive the discriminator, while the discriminator strives to improve its discrimination ability. This iterative process continues until the generator produces images that are visually convincing and indistinguishable from real images.\n# During training, the generator and discriminator networks are updated using techniques like stochastic gradient descent (SGD) or Adam optimization. The Binary Cross Entropy loss function is commonly used to compute the difference between predicted probabilities and target labels for both networks. </p>\n# </body>\n# </html>\n# \n# \n\n# %% [code] {\"execution\":{\"iopub.status.busy\":\"2023-10-17T18:02:05.985614Z\",\"iopub.execute_input\":\"2023-10-17T18:02:05.986461Z\",\"iopub.status.idle\":\"2023-10-17T18:02:06.002706Z\",\"shell.execute_reply.started\":\"2023-10-17T18:02:05.986427Z\",\"shell.execute_reply\":\"2023-10-17T18:02:06.001568Z\"}}\n# DCGAN Model Training Step with Discriminator and Generator\n\nclass DCGAN(keras.Model):\n    def __init__(self, generator, discriminator, latent_dim = input_dim):\n        super().__init__()\n        self.generator = generator\n        self.discriminator = discriminator\n        self.latent_dim = latent_dim\n        self.g_loss_metric = keras.metrics.Mean(name='g_loss')\n        self.d_loss_metric = keras.metrics.Mean(name='d_loss')\n        \n    @property\n    def metrics(self):\n        return [self.g_loss_metric, self.d_loss_metric]\n    \n    def compile(self, g_optimizer, d_optimizer, loss_fn):\n        super(DCGAN, self).compile()\n        self.g_optimizer = g_optimizer\n        self.d_optimizer = d_optimizer\n        self.loss_fn = loss_fn\n        \n    def train_step(self, real_images):\n        # get batch size from the data\n        batch_size = tf.shape(real_images)[0]\n        # generate random noise\n        random_noise = tf.random.normal(shape=(batch_size, self.latent_dim))\n        \n        # train the discriminator with real (1) and fake (0) images\n        with tf.GradientTape() as tape:\n            # compute loss on real images\n            pred_real = self.discriminator(real_images, training=True)\n            # generate real image labels\n            real_labels = tf.ones((batch_size, 1))\n            # label smoothing\n            real_labels += 0.05 * tf.random.uniform(tf.shape(real_labels))\n            d_loss_real = self.loss_fn(real_labels, pred_real)\n            \n            # compute loss on fake images\n            fake_images = self.generator(random_noise)\n            pred_fake = self.discriminator(fake_images, training=True)\n            # generate fake labels\n            fake_labels = tf.zeros((batch_size, 1))\n            d_loss_fake = self.loss_fn(fake_labels, pred_fake)\n            \n            # total discriminator loss\n            d_loss = (d_loss_real + d_loss_fake) / 2\n            \n        # compute discriminator gradients\n        gradients = tape.gradient(d_loss, self.discriminator.trainable_variables)\n        # update the gradients\n        self.d_optimizer.apply_gradients(zip(gradients, self.discriminator.trainable_variables))\n        \n        \n        # train the generator model\n        labels = tf.ones((batch_size, 1))\n        # generator want discriminator to think that fake images are real\n        with tf.GradientTape() as tape:\n            # generate fake images from generator\n            fake_images = self.generator(random_noise, training=True)\n            # classify images as real or fake\n            pred_fake = self.discriminator(fake_images, training=True)\n            # compute loss\n            g_loss = self.loss_fn(labels, pred_fake)\n            \n        # compute gradients\n        gradients = tape.gradient(g_loss, self.generator.trainable_variables)\n        # update the gradients\n        self.g_optimizer.apply_gradients(zip(gradients, self.generator.trainable_variables))\n        \n        # update states for both models\n        self.d_loss_metric.update_state(d_loss)\n        self.g_loss_metric.update_state(g_loss)\n        \n        return {'d_loss': self.d_loss_metric.result(), 'g_loss': self.g_loss_metric.result()}\n\n# %% [markdown]\n# <html>\n# <head>\n# </head>\n# <body>\n#   <h1> The Monitoring process </h1>\n#   <p> To monitor the training progress, callbacks like the DCGANMonitor can be used. This callback generates images from random noise using the trained generator and visualizes them. Additionally, the generator can be saved at the end of training for future use. </p>\n# </body>\n# </html>\n# \n# \n\n# %% [code] {\"execution\":{\"iopub.status.busy\":\"2023-10-17T18:02:06.004431Z\",\"iopub.execute_input\":\"2023-10-17T18:02:06.005303Z\",\"iopub.status.idle\":\"2023-10-17T18:02:06.021471Z\",\"shell.execute_reply.started\":\"2023-10-17T18:02:06.005272Z\",\"shell.execute_reply\":\"2023-10-17T18:02:06.020029Z\"}}\n# DCGAN Monitor for Image Generation and Model Saving\n\nclass DCGANMonitor(keras.callbacks.Callback):\n    def __init__(self, num_imgs=25, latent_dim = input_dim):\n        self.num_imgs = num_imgs\n        self.latent_dim = latent_dim\n        # create random noise for generating images\n        self.noise = tf.random.normal([25, latent_dim])\n\n    def on_epoch_end(self, epoch, logs = None):\n        # generate the image from noise\n        g_img = self.model.generator(self.noise)\n        # denormalize the image\n        g_img = (g_img * 255) + 255\n        g_img.numpy()\n        \n    def on_train_end(self, logs = None):\n        self.model.generator.save('DCGEN.h5')\n\n# %% [markdown] {\"execution\":{\"iopub.status.busy\":\"2023-10-11T17:25:02.771579Z\",\"iopub.execute_input\":\"2023-10-11T17:25:02.772215Z\",\"iopub.status.idle\":\"2023-10-11T17:25:02.780734Z\",\"shell.execute_reply.started\":\"2023-10-11T17:25:02.772183Z\",\"shell.execute_reply\":\"2023-10-11T17:25:02.77983Z\"}}\n# <a id=\"8\"></a>\n# # <p style=\"background-image: url(https://i.postimg.cc/K87ByXmr/stage5.jpg);font-family:camtasia;font-size:120%;color:white;text-align:center;border-radius:15px 50px; padding:7px\"> Train The Model </p>\n# <a class=\"btn\" href=\"#home\">Tabel of Contents</a>\n\n# %% [code] {\"execution\":{\"iopub.status.busy\":\"2023-10-17T18:02:06.023303Z\",\"iopub.execute_input\":\"2023-10-17T18:02:06.024985Z\",\"iopub.status.idle\":\"2023-10-17T19:30:53.451527Z\",\"shell.execute_reply.started\":\"2023-10-17T18:02:06.024926Z\",\"shell.execute_reply\":\"2023-10-17T19:30:53.450078Z\"}}\n# Training DCGAN on Image Dataset for 40 Epochs\n\nepochs = 30\nlr_g =0.0003\nlr_d = 0.0001\nbeta = 0.5\nlatent_dim = 300\n\ndcgan = DCGAN(generator=generator, discriminator=discriminator, latent_dim = latent_dim )\ndcgan.compile(g_optimizer = Adam (learning_rate= lr_g, beta_1= beta), d_optimizer= Adam (learning_rate = lr_g , beta_1= beta), loss_fn = BinaryCrossentropy())\n\n# Fit the model and save the history\nhistory = dcgan.fit(train_generator, epochs=epochs, callbacks=[DCGANMonitor()])\n\n\n# %% [markdown]\n# <a id=\"9\"></a>\n# # <p style=\"background-image: url(https://i.postimg.cc/K87ByXmr/stage5.jpg);font-family:camtasia;font-size:120%;color:white;text-align:center;border-radius:15px 50px; padding:7px\"> Evaluation Of Model Results </p>\n# <a class=\"btn\" href=\"#home\">Tabel of Contents</a>\n\n# %% [code] {\"execution\":{\"iopub.status.busy\":\"2023-10-17T19:30:53.453231Z\",\"iopub.execute_input\":\"2023-10-17T19:30:53.453838Z\",\"iopub.status.idle\":\"2023-10-17T19:30:57.556619Z\",\"shell.execute_reply.started\":\"2023-10-17T19:30:53.453798Z\",\"shell.execute_reply\":\"2023-10-17T19:30:57.555323Z\"}}\n# Generating 36 Random Images with DCGAN\n\nplt.figure(figsize=(10, 10))\n\nfor i in range(36):\n    plt.subplot(6, 6, i + 1)\n    # Generate random noise for each image\n    noise = tf.random.normal([1, 300])\n    mg = dcgan.generator(noise)\n    # Denormalize\n    mg = (mg * 255) + 255\n\n    mg.numpy()\n    image = Image.fromarray(np.uint8(mg[0]))\n\n    plt.imshow(image)\n    plt.axis('off')\n\nplt.show()\n\n# %% [code] {\"execution\":{\"iopub.status.busy\":\"2023-10-17T17:30:36.26451Z\",\"iopub.execute_input\":\"2023-10-17T17:30:36.265074Z\",\"iopub.status.idle\":\"2023-10-17T17:30:36.760791Z\"}}\nimport matplotlib.pyplot as plt\n\n# Function to create a figure for the losses\ndef create_loss_figure(d_loss_values, g_loss_values):\n    plt.figure(figsize=(10, 6))\n    plt.plot(d_loss_values, label='Discriminator Loss')\n    plt.plot(g_loss_values, label='Generator Loss')\n    plt.title('Generator and Discriminator Losses')\n    plt.xlabel('Epochs')\n    plt.ylabel('Loss')\n    plt.legend()\n    plt.grid(True)\n    plt.show()\n\n# Access the loss values from the history\nd_loss_values = history.history['d_loss']\ng_loss_values = history.history['g_loss']\n\n# Call the create_loss_figure function with the loss values\ncreate_loss_figure(d_loss_values, g_loss_values)\n\n# %% [markdown]\n# <a id=\"10\"></a>\n# # <p style=\"background-image: url(https://i.postimg.cc/K87ByXmr/stage5.jpg);font-family:camtasia;font-size:120%;color:white;text-align:center;border-radius:15px 50px; padding:7px\">Thank you for taking the time to review my notebook. If you have any questions or criticisms, please kindly let me know in the comments section.  </p>","metadata":{"_uuid":"941627f0-ed17-41cd-be1c-27badce62a21","_cell_guid":"8682aecb-58d7-4d65-aac8-e3ed3a819ac8","collapsed":false,"jupyter":{"outputs_hidden":false},"execution":{"iopub.status.busy":"2024-08-24T20:53:11.354325Z","iopub.execute_input":"2024-08-24T20:53:11.354591Z","iopub.status.idle":"2024-08-24T20:53:11.402944Z","shell.execute_reply.started":"2024-08-24T20:53:11.354565Z","shell.execute_reply":"2024-08-24T20:53:11.401815Z"},"trusted":true},"execution_count":1,"outputs":[{"traceback":["\u001b[0;36m  Cell \u001b[0;32mIn[1], line 54\u001b[0;36m\u001b[0m\n\u001b[0;31m    <a id=\"3\"></a>\u001b[0m\n\u001b[0m    ^\u001b[0m\n\u001b[0;31mSyntaxError\u001b[0m\u001b[0;31m:\u001b[0m invalid syntax\n"],"ename":"SyntaxError","evalue":"invalid syntax (68618419.py, line 54)","output_type":"error"}]}]}