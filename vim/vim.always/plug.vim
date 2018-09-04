
call plug#begin('~/.vim/plugged')

" Colorschemes
Plug 'captbaritone/molokai'
Plug 'altercation/vim-colors-solarized'
Plug 'ajh17/spacegray.vim'
Plug 'jpo/vim-railscasts-theme'
Plug 'vim-scripts/xoria256.vim'

" Syntax
Plug 'darfink/vim-plist', { 'for': 'plist'}
Plug 'elzr/vim-json', { 'for': 'json'}
Plug 'tpope/vim-git', { 'for': 'git' }
Plug 'plasticboy/vim-markdown', { 'for': 'markdown' }
Plug 'vhda/verilog_systemverilog.vim'
Plug 'alisdair/vim-armasm'

" Fancy statusline
Plug 'bling/vim-airline'
Plug 'vim-airline/vim-airline-themes'
" Plug 'itchyny/lightline.vim'

" Fuzzy file opener
Plug 'ctrlpvim/ctrlp.vim'
Plug 'junegunn/fzf.vim'

" Navigate files in a sidebar
Plug 'scrooloose/nerdtree'

" Change brackets and quotes
Plug 'tpope/vim-surround'

" Make vim-surround repeatable with .
Plug 'tpope/vim-repeat'

" Turns esc sequences into colors in vim
Plug 'jbnicolai/vim-AnsiEsc'

Plug 'adelarsq/vim-matchit'
Plug 'Raimondi/delimitMate'
Plug 'easymotion/vim-easymotion'
" Plug 'tpope/vim-commentary'
Plug 'tomtom/tcomment_vim'
Plug 'AndrewRadev/switch.vim'

Plug 'Valloric/YouCompleteMe'

call plug#end()
