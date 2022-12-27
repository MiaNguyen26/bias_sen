
# **EDA for sentiment data**


## **Preprocessing**

- Input: 
    Dataframe which includes *text* column. This column is preprocessed later
- Output:
A new dataframe which has the same columns as the original df, and added some new columns below:
    - *token* : using pyvi.tokenization for *** raw *text* *** (I)
        > Gia_đình tôi rất hài_lòng về dịch_vụ của khách_sạn
    - *spacy_token* : using pyvi.spacy_tokenize for *** raw *text* *** (J)
        > ['Gia_đình', 'tôi', 'rất', 'hài_lòng', 'về', 'dịch_vụ', 'của', 'khách_sạn']
    - *pos* : using POS tagging token for *spacy token* (K)
        > (['Gia_đình', 'tôi', 'rất', 'hài_lòng', 'về', 'dịch_vụ', 'của', 'khách_sạn'], ['N', 'P', 'R', 'A', 'E', 'N', 'E', 'N'])
    - *lower* : lower the **spacy_token** results (L)
        > ['gia_đình', 'tôi', 'rất', 'hài_lòng', 'về', 'dịch_vụ', 'của', 'khách_sạn']
    - *no_punc* : remove puntuation of lowering results (M)
        > ['gia_đình', 'tôi', 'rất', 'hài_lòng', 'về', 'dịch_vụ', 'của', 'khách_sạn']
    - *no_emoij* : remove emojis (N)
        > ['gia_đình', 'tôi', 'rất', 'hài_lòng', 'về', 'dịch_vụ', 'của', 'khách_sạn']
    - *processed* : the final results after removing some specific characters such as * '', '...' * (O)
        > ['gia_đình', 'tôi', 'rất', 'hài_lòng', 'về', 'dịch_vụ', 'của', 'khách_sạn']

