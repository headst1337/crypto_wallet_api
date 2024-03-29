import re
from typing import Optional, Tuple

from bip_utils import (
    MoneroSeedGenerator,
    Bip39SeedGenerator,
    MoneroLanguages,
    Bip39MnemonicGenerator,
    Bip39WordsNum,
    Bip39Languages,
    MoneroMnemonicGenerator,
    MoneroWordsNum,
    MoneroLanguages
)


def generate_mnemonic_seed( 
    lang: str = None,  
    length: int = None, 
    mnemonic: Optional[str] = None
) -> Tuple[bytes, str]:
    
    if mnemonic is None:
        mnemonic = str(generate_mnemonic(lang, length))

    if re.search('[а-яА-Я]', str(mnemonic)):
        lang = 'ru'
    else:
        lang = 'en'

    if lang == 'ru':
        seed = MoneroSeedGenerator(mnemonic, MoneroLanguages.RUSSIAN).Generate()
    else:
        seed = Bip39SeedGenerator(mnemonic).Generate()
    return seed, mnemonic


def generate_mnemonic(lang: str, length: int):
    if lang == 'ru':
        words_num = {
            12: MoneroWordsNum.WORDS_NUM_12,
            24: MoneroWordsNum.WORDS_NUM_24,
        }.get(length, MoneroWordsNum.WORDS_NUM_12)
        return MoneroMnemonicGenerator(MoneroLanguages.RUSSIAN).FromWordsNumber(words_num)
    else:
        words_num = {
            12: Bip39WordsNum.WORDS_NUM_12,
            24: Bip39WordsNum.WORDS_NUM_24
        }.get(length, Bip39WordsNum.WORDS_NUM_12)
        return Bip39MnemonicGenerator(Bip39Languages.ENGLISH).FromWordsNumber(words_num)
    