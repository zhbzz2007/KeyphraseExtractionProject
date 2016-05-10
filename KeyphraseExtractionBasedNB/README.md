## 程序流程 ##

### 1.预处理 ###

预处理模块主要用于分句、分词、词性标注，以及抽取候选短语；

测试文件，preProcessTest.py

实现文件，Preprocess\preProcess.py


### 2.特征选择 ###

特征选择主要用于计算tf、idf、位置等信息，构建每个短语的特征向量及类标签；

为了保证速度，idf需要预先离线计算，主要计算每个单词、候选短语、结果短语的idf值，（第一次需要执行，后续按照需要选择执行，IdfTrainTest.py）；

测试文件，SelectFeatureTest.py

实现文件，FeatureSelection\SelectFeature.py

### 3.关键短语抽取 ###

1. 分割数据集；
2. 训练Naive Bayes分类器；
3. 验证Naive Bayes分类器；
4. 利用Naive Bayes分类器进行关键短语抽取，对每一篇文档中的候选短语进行分类，如果标签为1，则为关键短语；

测试文件，KeyphraseExtractionTest.py

实现文件，Classifier\NaiveBayes.py