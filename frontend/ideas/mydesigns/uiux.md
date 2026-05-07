.c360-tabs--floating{
    /* align-items: stretch; */
    width: 100%;
}
.c360-tabs--floating.c360-tabs--floating-bottom .c360-tabs__list--floating-wrap{
    z-index: var(--c360-z-dropdown);
    /* left: 0; */
    /* right: 0; */
    width: min-content;
    /* max-width: none; */
    box-shadow: var(--c360-shadow-md);
    bottom: calc(var(--c360-spacing-3) + env(safe-area-inset-bottom, 0px));
    margin: 0;
    padding: 3px 2px;
    position: fixed;
    transform: none;
}
.c360-tabs--floating .c360-tabs__list--floating-wrap{
        /* width: 100%; */
    /* max-width: 100%; */
    padding: var(--c360-spacing-2) var(--c360-spacing-1);
    background: var(--c360-bg-elevated);
    border: 1px solid var(--c360-border-strong);
    box-shadow: var(--c360-shadow-lg);
    box-sizing: border-box;
    border-radius: 5px;
    margin: 0 auto;
    position: relative;
}

.c360-tabs--floating .c360-tabs__tab{
        z-index: 1;
    justify-content: center;
    align-items: center;
    gap: var(--c360-spacing-1);
    /* min-width: min(120px, 22vw); */
    padding: var(--c360-spacing-2) var(--c360-spacing-2);
    font-size: var(--c360-text-xs);
    color: var(--c360-text-muted);
    border-bottom: none;
    flex-direction: column;
    flex: auto;
    margin-bottom: 0;
    position: relative;
    width: 100px;
}




























