wiki.theme = {};

wiki.theme.bodyEl = document.body;
wiki.theme.html = document.documentElement;

wiki.theme.viewportHeight;
wiki.theme.tableOfContents = document.querySelector('.table-of-contents');
wiki.theme.tableOfContentsContainer = document.querySelector('.columns-table-of-contents');
wiki.theme.searchResults = document.getElementById('mkdocs-search-results');
wiki.theme.page404 = document.getElementById('page404');
wiki.theme.mainSection = document.querySelector('.main');
wiki.theme.mainSectionHeight;
wiki.theme.headerSection = document.querySelector('.header');
wiki.theme.headerSectionHeight;
wiki.theme.sticky = wiki.theme.tableOfContentsContainer.offsetTop;
wiki.theme.stickyController = wiki.theme.mainSection.offsetTop;
wiki.theme.internalLinks = wiki.theme.tableOfContents.querySelectorAll('a');
wiki.theme.contentsEl = document.querySelector('.contents');
wiki.theme.images = wiki.theme.contentsEl.querySelectorAll('img');

wiki.theme.toggleModalImg = function() {
  wiki.theme.bodyEl.classList.toggle('show-modal-img');
}

wiki.theme.toggleDocsNav = function() {
  wiki.theme.bodyEl.classList.toggle("show-docs-nav");
}

wiki.theme.toggleNavChild = function(e) {
  e = e || window.event;
  let targ = e.target || e.srcElement || e;
  if (targ.nodeType == 3) targ = targ.parentNode;
  let parent = targ.parentElement;
  parent.classList.toggle("show-nav-child");
}

wiki.theme.onScroll = function() {
  let scrollValue = window.scrollY || window.scrollTop || document.querySelector('html').scrollTop;
  if (wiki.theme.mainSectionHeight >= (wiki.theme.viewportHeight*2)) {
    if (scrollValue >= wiki.theme.stickyController) {
      wiki.theme.tableOfContentsContainer.classList.add("sticky");
    } else {
      wiki.theme.tableOfContentsContainer.classList.remove("sticky");
    }
    if (scrollValue >= ((wiki.theme.mainSectionHeight + wiki.theme.headerSectionHeight) - wiki.theme.viewportHeight)) {
      wiki.theme.tableOfContentsContainer.classList.add("hide");
    } else {
      wiki.theme.tableOfContentsContainer.classList.remove("hide");
    }
  }
}

wiki.theme.internalLinks.forEach(function(link) {
  link.onclick = function(e) {
    e = e || window.event;
    let targ = e.target || e.srcElement || e;
    if (targ.nodeType == 3) targ = targ.parentNode;
    let internalLinksHref = targ.getAttribute("href");
    let internalAnchorId = internalLinksHref.replace('#','');
    let titleEl = document.getElementById(internalAnchorId);
    titleEl.classList.add("highlight");
    setTimeout(function(){
      titleEl.classList.remove("highlight");
    }, 1200);
  };
});

/**
 * 
 * Use images title as caption
 */
wiki.theme.images.forEach(function(image) {
  let title = image.getAttribute('title');
  if (title) {
    let imageContainer = image.parentNode;
    let caption = imageContainer.querySelector('figcaption');
    if (!caption) {
      caption = document.createElement('figcaption');
      caption.innerHTML = title;
      imageContainer.insertBefore(caption, image.nextSibling);
    }
  }
  image.onclick = function(e) {
    let targ = e.target || e.srcElement || e;
    if (targ.nodeType == 3) targ = targ.parentNode;
    e = e || window.event;
    if (targ.alt != "inline-icon") {
      let modal = document.querySelector('.modal');
      modal.classList.add('modal-zoomed-img');
      let contents = [];
      let imgModal = document.createElement('div');
      imgModal.setAttribute('id', 'modal-inner-content-image');
      let src = targ.src;
      let alt = targ.alt;
      let classList = targ.classList;
      imgModal.innerHTML = "<img src='" + src + "' class='" + classList + "' alt='" + alt + "'>";
      contents.push(imgModal);
      let cfg = {
        contents: contents,
        additionalCls: 'show-modal-zoomed-img'
      };
      wiki.modal.buildModal(cfg);      
    }
  };
});

window.addEventListener("scroll", wiki.theme.onScroll);

wiki.theme.bodyEl.onresize = function() {
  wiki.theme.viewportHeight = Math.max(document.documentElement.clientHeight || 0, window.innerHeight || 0);
  wiki.theme.mainSectionHeight = wiki.theme.mainSection.clientHeight;
  wiki.theme.headerSectionHeight = wiki.theme.headerSection.clientHeight;
};

wiki.theme.bodyEl.onload = function() {
  wiki.theme.mainSectionHeight = wiki.theme.mainSection.clientHeight;
  wiki.theme.headerSectionHeight = wiki.theme.headerSection.clientHeight;
  wiki.theme.viewportHeight = Math.max(document.documentElement.clientHeight || 0, window.innerHeight || 0);
  let navChild = document.querySelectorAll('.nav-child');
  navChild.forEach(function(item) {
    let navChildItemActive = item.querySelectorAll('.active');
    if (navChildItemActive.length) {
      item.parentElement.classList.add('show-nav-child');
    }
  });

  if (wiki.theme.page404) {
    wiki.theme.bodyEl.classList.add("page-404");
  }
  if (wiki.theme.searchResults) {
    wiki.theme.bodyEl.classList.add("search-page");
  }
}
