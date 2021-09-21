import seaborn as sns
import matplotlib.pyplot as plt


class Visualizer():
    def __init__(self, learner):
        self.learner = learner
        self.IOManager = learner.IOManager
        self.config = learner.config

    # 保存画图用的参数
    def initialize(self):
        self.step_log_interval = []
        self.train_metric_record = []
        self.train_loss_record = []
        self.step_valid_interval = []
        self.valid_metric_record = []
        self.valid_loss_record = []
        self.step_test_interval = []
        self.test_metric_record = []
        self.test_loss_record = []
        self.roc_data = None
        self.prc_data = None

    # 四张图Train Acc Curve、Train Loss Curve、Test Acc Curve、Test Loss Curve
    def draw_train_test_curve(self):
        sns.set(style="darkgrid")
        plt.figure(22, figsize=(16, 12))
        plt.subplots_adjust(wspace=0.2, hspace=0.3)

        plt.subplot(2, 2, 1)
        plt.title("Train Acc Curve", fontsize=23)
        plt.xlabel("Step", fontsize=20)
        plt.ylabel("Accuracy", fontsize=20)
        plt.plot(self.step_log_interval, self.train_metric_record)
        plt.subplot(2, 2, 2)
        plt.title("Train Loss Curve", fontsize=23)
        plt.xlabel("Step", fontsize=20)
        plt.ylabel("Loss", fontsize=20)
        plt.plot(self.step_log_interval, self.train_loss_record)
        plt.subplot(2, 2, 3)
        plt.title("Test Acc Curve", fontsize=23)
        plt.xlabel("Epoch", fontsize=20)
        plt.ylabel("Accuracy", fontsize=20)
        plt.plot(self.step_test_interval, self.test_metric_record)
        plt.subplot(2, 2, 4)
        plt.title("Test Loss Curve", fontsize=23)
        plt.xlabel("Step", fontsize=20)
        plt.ylabel("Loss", fontsize=20)
        plt.plot(self.step_test_interval, self.test_loss_record)

        plt.savefig('{}/{}.{}'.format(self.IOManager.result_path, self.config.learn_name, self.config.save_figure_type))
        plt.show()

    def draw_ROC_PRC_curve(self):
        # roc_data = [FPR, TPR, AUC]
        # prc_data = [recall, precision, AP]
        sns.set(style="darkgrid")
        plt.figure(figsize=(16, 8))
        plt.subplots_adjust(wspace=0.2, hspace=0.3)
        lw = 2

        plt.subplot(1, 2, 1)
        plt.plot(self.step_log_interval, self.train_metric_record)
        plt.plot(self.roc_data[0], self.roc_data[1], color='darkorange',
                 lw=lw, label='ROC curve (area = %0.2f)' % self.roc_data[2])  ### 假正率为横坐标，真正率为纵坐标做曲线
        plt.plot([0, 1], [0, 1], color='navy', lw=lw, linestyle='--')
        plt.xlim([0.0, 1.0])
        plt.ylim([0.0, 1.05])
        plt.xlabel('False Positive Rate', fontdict={'weight': 'normal', 'size': 20})
        plt.ylabel('True Positive Rate', fontdict={'weight': 'normal', 'size': 20})
        plt.title('receiver operating characteristic curve', fontdict={'weight': 'normal', 'size': 23})
        plt.legend(loc="lower right", prop={'weight': 'normal', 'size': 18})

        plt.subplot(1, 2, 2)
        # plt.step(self.prc_data[0], self.prc_data[1], color='b', alpha=0.2,
        #          where='post')
        plt.plot(self.prc_data[0], self.prc_data[1], color='darkorange',
                 lw=lw, label='PR curve (area = %0.2f)' % self.prc_data[2])  ### 假正率为横坐标，真正率为纵坐标做曲线
        plt.fill_between(self.prc_data[0], self.prc_data[1], step='post', alpha=0.2,
                         color='b')
        plt.xlabel('Recall',fontdict={'weight': 'normal', 'size': 20})
        plt.ylabel('Precision',fontdict={'weight': 'normal', 'size': 20})
        plt.plot([0, 1], [1, 0], color='navy', lw=lw, linestyle='--')
        plt.ylim([0.0, 1.05])
        plt.xlim([0.0, 1.05])
        plt.title('Precision Recall curve', fontdict={'weight': 'normal', 'size': 20})
        plt.legend(loc="lower left", prop={'weight': 'normal', 'size': 18})

        plt.savefig('{}/{}.{}'.format(self.IOManager.result_path, self.config.learn_name+'ROC_PRC', self.config.save_figure_type))
        plt.show()
