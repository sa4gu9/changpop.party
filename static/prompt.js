function btnClick(name) {
  const element = document.getElementsByName(name + "_div")[0];
  console.log(element);
  element.hidden = !element.hidden;
}
