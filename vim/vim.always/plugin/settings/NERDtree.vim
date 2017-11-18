" Make nerdtree look nice
let NERDTreeMinimalUI = 1
let NERDTreeDirArrows = 1



" maybe: changing the cwd let NERDTreeChDirMode=2
let NERDTreeIgnore=['\~$', '\.pyc$', '\.swp$']

" XXX: the last two entries are filtered already, no?"
let NERDTreeSortOrder=['^__\.py$', '\/$', '*', '\.swp$',  '\~$']



" keys
" ===========
noremap <F2> :NERDTreeToggle<CR>

" Open the project tree and expose current file in the nerdtree with Shift-F2
noremap <silent> <S-F2> :NERDTreeFind<CR>:vertical res 30<CR>
"
