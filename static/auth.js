function hash(string) {
  const utf8 = new TextEncoder().encode(string);
  return crypto.subtle.digest('SHA-256', utf8).then((hashBuffer) => {
    const hashArray = Array.from(new Uint8Array(hashBuffer));
    const hashHex = hashArray
      .map((bytes) => bytes.toString(16).padStart(2, '0'))
      .join('');
    return hashHex;
  });
}
async function auth() {
    if (localStorage.getItem("UserName")) {
        console.log(localStorage.getItem("UserName"))
    } else {
        console.log("no userName found")
        localStorage.setItem("UserName", prompt("UserName:"))
    }
    if (localStorage.getItem("Hash")) {
        //console.log(localStorage.getItem("Hash"))
    } else {
        console.log("no Hash found")
        let Hash = await hash(localStorage.getItem("UserName")+":"+prompt("Password for"+localStorage.getItem("UserName")+":"))
        //console.log(Hash)
        localStorage.setItem("Hash", Hash)
    }
    console.log(window.location)
    if (window.location.href.includes("?hash")) {
        console.log(true)
    }else {
    window.location.replace(window.location.href+"?hash="+localStorage.getItem("Hash")+"&user="+localStorage.getItem("UserName"))
}}
auth()