# Answers to grade by hand (judge verdicts are not shown here)

## q01 (single)
**Question:** What iteration count should I use for PBKDF2 with HMAC-SHA256?
**Reference:** 600,000 iterations (220,000 for PBKDF2-HMAC-SHA512; SHA1 is legacy only).
**Answer:** For PBKDF2 with HMAC-SHA256, you should use **600,000 iterations** (recommended) [Password_Storage_Cheat_Sheet:014]. If FIPS-140 compliance is required, set the work factor to 600,000 or more [Password_Storage_Cheat_Sheet:001].
**Retrieved passages:**
- [Password_Storage_Cheat_Sheet:014] Password Storage Cheat Sheet > Password Hashing Algorithms > PBKDF2: Since PBKDF2 is permitted by NIST SP 800-63B-4 and has FIPS-140 validated implementations, it should be the preferred algorithm when these are required.

The PBKDF2 algorithm requires that you select an internal hashing algorithm such as an HMAC or a variety of other hashing algorithms. HMAC-SHA-256 is widely supported and is recommended by NIST.

The work factor for PBKDF2 is implemented through ...
- [Password_Storage_Cheat_Sheet:007] Password Storage Cheat Sheet > Methods for Enhancing Password Storage > Using Work Factors: The work factor is the number of iterations of the hashing algorithm that are performed for each password (usually, it's actually `2^work` iterations). The work factor is typically stored in the hash output. It makes calculating the hash more computationally expensive, which in turn reduces the speed and/or increases the cost for which an attacker can attempt to crack the password hash.

When you ...
- [Password_Storage_Cheat_Sheet:015] Password Storage Cheat Sheet > Password Hashing Algorithms > Parallel PBKDF2 > PBKDF2 Pre-Hashing: - PPBKDF2-SHA512: cost 2
- PPBKDF2-SHA256: cost 5
- PPBKDF2-SHA1: cost 10

These configuration settings are equivalent in the defense they provide. (Number as of December 2022, based on testing of RTX 4000 GPUs)

When PBKDF2 is used with an HMAC, and the password is longer than the hash function's block size (64 bytes for SHA-256), the password will be automatically pre-hashed. For example, the pa...
- [Password_Storage_Cheat_Sheet:001] Password Storage Cheat Sheet > Introduction: This cheat sheet advises you on the proper methods for storing passwords for authentication. When passwords are stored, they must be protected from an attacker even if the application or database is compromised. Fortunately, a majority of modern languages and frameworks provide built-in functionality to help store passwords safely.

Passwords should never be stored in plain text. Instead, they mus...
- [Password_Storage_Cheat_Sheet:012] Password Storage Cheat Sheet > Password Hashing Algorithms > bcrypt > Input Limits of bcrypt: The bcrypt password hashing function **should only** be used for password storage in legacy systems where Argon2 and scrypt are not available.

The work factor should be as large as verification server performance will allow, with a minimum of 10.

bcrypt has a maximum length input length of 72 bytes for most implementations, so you should enforce a maximum password length of 72 bytes (or less if ...

## q02 (single)
**Question:** What maximum password length should I enforce if I hash passwords with bcrypt?
**Reference:** 72 bytes (or less if the implementation's limit is smaller); use a work factor of at least 10.
**Answer:** You should enforce a maximum password length of **72 bytes** (or less if the specific bcrypt implementation in use has smaller limits) [Password_Storage_Cheat_Sheet:012].
**Retrieved passages:**
- [Password_Storage_Cheat_Sheet:012] Password Storage Cheat Sheet > Password Hashing Algorithms > bcrypt > Input Limits of bcrypt: The bcrypt password hashing function **should only** be used for password storage in legacy systems where Argon2 and scrypt are not available.

The work factor should be as large as verification server performance will allow, with a minimum of 10.

bcrypt has a maximum length input length of 72 bytes for most implementations, so you should enforce a maximum password length of 72 bytes (or less if ...
- [Password_Storage_Cheat_Sheet:001] Password Storage Cheat Sheet > Introduction: This cheat sheet advises you on the proper methods for storing passwords for authentication. When passwords are stored, they must be protected from an attacker even if the application or database is compromised. Fortunately, a majority of modern languages and frameworks provide built-in functionality to help store passwords safely.

Passwords should never be stored in plain text. Instead, they mus...
- [Password_Storage_Cheat_Sheet:007] Password Storage Cheat Sheet > Methods for Enhancing Password Storage > Using Work Factors: The work factor is the number of iterations of the hashing algorithm that are performed for each password (usually, it's actually `2^work` iterations). The work factor is typically stored in the hash output. It makes calculating the hash more computationally expensive, which in turn reduces the speed and/or increases the cost for which an attacker can attempt to crack the password hash.

When you ...
- [Password_Storage_Cheat_Sheet:013] Password Storage Cheat Sheet > Password Hashing Algorithms > bcrypt > Pre-Hashing Passwords with bcrypt: An alternative approach is to pre-hash the user-supplied password with a fast algorithm such as SHA-2, HMAC, or BLAKE3 and then to hash the resulting hash value with bcrypt (i.e., `bcrypt(H($password)), $salt, $cost)`)..
This can be **dangerous** because of null bytes in the hash output value and because of password shucking.

The original bcrypt expects a null terminated password string, this mea...
- [Authentication_Cheat_Sheet:004] Authentication Cheat Sheet > Authentication General Guidelines > Implement Proper Password Strength Controls: - Password Length - **Minimum** length for passwords should be enforced by the application. - If MFA is enabled passwords **shorter than 8 characters** are considered to be weak (NIST SP800-63B). - If MFA is not enabled passwords **shorter than 15 characters** are considered to be weak (NIST SP800-63B). - **Maximum** password length should be **at least 64 characters** to allow passphrases (NIST S...

## q03 (single)
**Question:** Where should a password pepper be stored?
**Reference:** Not with the hashes: separately from the password database, as a secret in a secrets vault or HSM.
**Answer:** A password pepper should **not** be stored along with the generated hash or in the password database [Password_Storage_Cheat_Sheet:005]. 

Instead, it should be stored separately in a secrets vault or a Hardware Security Module (HSM) [Password_Storage_Cheat_Sheet:005].
**Retrieved passages:**
- [Password_Storage_Cheat_Sheet:005] Password Storage Cheat Sheet > Methods for Enhancing Password Storage > Peppering > Common requirements for peppering strategies: Peppering is a class of strategies that can be used in addition to salting to provide an additional layer of protection. It prevents an attacker from being able to crack any of the hashes if they only have access to the database, for example, if they have exploited a SQL injection vulnerability or obtained a backup of the database.

- A pepper is **shared between stored passwords**, rather than be...
- [Password_Storage_Cheat_Sheet:006] Password Storage Cheat Sheet > Methods for Enhancing Password Storage > Peppering > Post-hashing peppers: In this strategy, a pepper is added to a password before being hashed by a password hashing algorithm. The computed hash is then stored in the database. In this case the pepper should be a random value generated securely. See the Cryptographic_Storage_Cheat_Sheet for more information on securely generating random values.

In this strategy, a password is hashed as usual using a password hashing alg...
- [Password_Storage_Cheat_Sheet:001] Password Storage Cheat Sheet > Introduction: This cheat sheet advises you on the proper methods for storing passwords for authentication. When passwords are stored, they must be protected from an attacker even if the application or database is compromised. Fortunately, a majority of modern languages and frameworks provide built-in functionality to help store passwords safely.

Passwords should never be stored in plain text. Instead, they mus...
- [Password_Storage_Cheat_Sheet:002] Password Storage Cheat Sheet > Background > Hashing vs Encryption: Hashing and encryption can keep sensitive data safe, but in almost all circumstances, **Passwords should be securely hashed using modern, adaptive hashing algorithms (e.g., Argon2id, bcrypt, or PBKDF2), rather than encrypted or stored in plaintext.**

Because **hashing is a one-way function** (i.e., it is impossible to "decrypt" a hash and obtain the original plaintext value), it is the most appro...
- [Authentication_Cheat_Sheet:006] Authentication Cheat Sheet > Authentication General Guidelines > Store Passwords in a Secure Fashion: - ASVS v5.0 Password Security Requirements
- Passwords Evolved: Authentication Guidance for the Modern Era

It is common for an application to have a mechanism that provides a means for a user to gain access to their account in the event they forget their password. Please see Forgot Password Cheat Sheet for details on this feature.

It is critical for an application to store a password using the r...

## q04 (single)
**Question:** How much entropy does a session ID need?
**Reference:** At least 64 bits, generated with a cryptographically secure random number generator (CSPRNG).
**Answer:** Session IDs must have at least **64 bits** of entropy to prevent brute-force guessing attacks [Session_Management_Cheat_Sheet:005]. 

When creating custom session tokens or identifiers/secret verifiers, use a Cryptographically Secure Pseudorandom Number Generator (CSPRNG) with at least **128 bits** of entropy (and prefer 160 bits or more) [Session_Management_Cheat_Sheet:007, Session_Management_Cheat_Sheet:010].
**Retrieved passages:**
- [Session_Management_Cheat_Sheet:005] Session Management Cheat Sheet > Session ID Properties > Session ID Entropy: Session identifiers must have at least `64 bits` of entropy to prevent brute-force session guessing attacks. Entropy refers to the amount of randomness or unpredictability in a value. Each “bit” of entropy doubles the number of possible outcomes, meaning a session ID with 64 bits of entropy can have `2^64` possible values.

A strong CSPRNG (Cryptographically Secure Pseudorandom Number Generator) m...
- [Session_Management_Cheat_Sheet:006] Session Management Cheat Sheet > Session ID Properties > Session ID Length: As mentioned in the previous *Session ID Entropy* section, a primary security requirement for session IDs is that they contain at least `64 bits` of entropy to prevent brute-force guessing attacks. Although session ID length matters, it's the entropy that ensures security. The session ID must be long enough to encode sufficient entropy, preventing brute force attacks where an attacker guesses vali...
- [Session_Management_Cheat_Sheet:003] Session Management Cheat Sheet > Session ID Properties: In order to keep the authenticated state and track the users progress within the web application, applications provide users with a **session identifier** (session ID or token) that is assigned at session creation time, and is shared and exchanged by the user and the web application for the duration of the session (it is sent on every HTTP request). The session ID is a `name=value` pair.

With the...
- [Session_Management_Cheat_Sheet:007] Session Management Cheat Sheet > Session ID Properties > Session ID Content (or Value): The session ID content (or value) must be meaningless to prevent information disclosure attacks, where an attacker is able to decode the contents of the ID and extract details of the user, the session, or the inner workings of the web application.

The session ID must simply be an identifier on the client side, and its value must never include sensitive information or Personally Identifiable Infor...
- [Session_Management_Cheat_Sheet:010] Session Management Cheat Sheet > Session Management Implementation > Server-Side Session Token Storage: Storing random session tokens verbatim can be acceptable in a tightly controlled session store, but anyone who can read it can reuse unexpired tokens. High entropy protects against guessing; it does not protect exposed tokens. If read-only disclosure of the store is in your threat model, store a one-way verifier instead. RFC 6819 recommends token hashes for the corresponding OAuth access-token dat...

## q05 (single)
**Question:** Which cookie name prefix should I use for the session ID cookie and what does it require?
**Reference:** __Host-: the cookie must be Secure, have no Domain attribute and use Path=/.
**Answer:** It is recommended to use the `__Host-` prefix for session ID cookies [Session_Management_Cheat_Sheet:017]. 

Requirements:
- The cookie must be set with `Secure` [Session_Management_Cheat_Sheet:017].
- It must not have a `Domain` attribute [Session_Management_Cheat_Sheet:017].
- It must use `Path=/` [Session_Management_Cheat_Sheet:017].

If subdomain sharing is required, you can use the `__Secure-` prefix instead, which requires the cookie to be set with `Secure` [Session_Management_Cheat_Sheet:017].
**Retrieved passages:**
- [Session_Management_Cheat_Sheet:017] Session Management Cheat Sheet > Cookies > Cookie Name Prefixes: Use cookie name prefixes to bind cookies to security properties at the browser level (RFC 6265bis §4.1.3):

- `__Host-` — the cookie must be set with `Secure`, must not have a `Domain` attribute, and must use `Path=/`. Prevents subdomain forgery and HTTPS downgrade attacks. **Recommended for session IDs.**
- `__Secure-` — the cookie must be set with `Secure`. Use only when subdomain sharing is req...
- [Session_Management_Cheat_Sheet:004] Session Management Cheat Sheet > Session ID Properties > Session ID Name Fingerprinting: The name used by the session ID should not be extremely descriptive nor offer unnecessary details about the purpose and meaning of the ID.

The session ID names used by the most common web application development frameworks can be easily fingerprinted, such as `PHPSESSID` (PHP), `JSESSIONID` (J2EE), `CFID` & `CFTOKEN` (ColdFusion), `ASP.NET_SessionId` (ASP .NET), etc. Therefore, the session ID nam...
- [Session_Management_Cheat_Sheet:003] Session Management Cheat Sheet > Session ID Properties: In order to keep the authenticated state and track the users progress within the web application, applications provide users with a **session identifier** (session ID or token) that is assigned at session creation time, and is shared and exchanged by the user and the web application for the duration of the session (it is sent on every HTTP request). The session ID is a `name=value` pair.

With the...
- [Session_Management_Cheat_Sheet:008] Session Management Cheat Sheet > Session Management Implementation: The session management implementation defines the exchange mechanism that will be used between the user and the web application to share and continuously exchange the session ID. There are multiple mechanisms available in HTTP to maintain session state within web applications, such as cookies (standard HTTP header), URL parameters (URL rewriting – RFC2396), URL arguments on GET requests, body argu...
- [Session_Management_Cheat_Sheet:011] Session Management Cheat Sheet > Session Management Implementation > Used vs. Accepted Session ID Exchange Mechanisms: A web application should make use of cookies for session ID exchange management. If a user submits a session ID through a different exchange mechanism, such as a URL parameter, the web application should avoid accepting it as part of a defensive strategy to stop session fixation.

**NOTE**:

- Even if a web application makes use of cookies as its default session ID exchange mechanism, it might acc...

## q06 (single)
**Question:** Which SameSite value should my session cookie use?
**Reference:** SameSite=Strict (preferred) or Lax, set explicitly; never None without Secure; it is defense in depth, not a replacement for CSRF tokens.
**Answer:** Your session cookie must explicitly set `SameSite=Strict` (preferred) or `SameSite=Lax` [Session_Management_Cheat_Sheet:016]:

* **`SameSite=Strict` (Preferred):** Excludes cross-site requests entirely, preventing the cookie from being sent even when following external links [Session_Management_Cheat_Sheet:016, Cross-Site_Request_Forgery_Prevention_Cheat_Sheet:025]. 
* **`SameSite=Lax`:** Permits top-level cross-site navigations using safe HTTP methods (such as following a link), balancing security and usability [Session_Management_Cheat_Sheet:016, Cross-Site_Request_Forgery_Prevention_Cheat_Sheet:025].

Do not rely on browser-default values, and never use `SameSite=None` without `Secure` [Session_Management_Cheat_Sheet:016].
**Retrieved passages:**
- [Session_Management_Cheat_Sheet:016] Session Management Cheat Sheet > Cookies > SameSite Attribute: The `SameSite` attribute controls whether browsers send a cookie with cross-site requests. `SameSite=Strict` excludes cross-site requests, while `SameSite=Lax` permits top-level cross-site navigations that use safe HTTP methods. Treat `SameSite` as defense in depth against CSRF, not as a replacement for a CSRF token. Session cookies must explicitly set `SameSite=Strict` (preferred) or `SameSite=La...
- [Cross-Site_Request_Forgery_Prevention_Cheat_Sheet:025] Cross-Site Request Forgery Prevention Cheat Sheet > Defense In Depth Techniques > SameSite (Cookie Attribute): `SameSite` is a cookie attribute that controls whether browsers send cookies with cross-site requests. It is defined in RFC6265bis and takes one of three values:

- `Strict` prevents cookies from being sent with cross-site requests, including top-level navigations from external links. This can disrupt legitimate navigation into an application.
- `Lax` sends cookies on cross-site top-level navigati...
- [Session_Management_Cheat_Sheet:017] Session Management Cheat Sheet > Cookies > Cookie Name Prefixes: Use cookie name prefixes to bind cookies to security properties at the browser level (RFC 6265bis §4.1.3):

- `__Host-` — the cookie must be set with `Secure`, must not have a `Domain` attribute, and must use `Path=/`. Prevents subdomain forgery and HTTPS downgrade attacks. **Recommended for session IDs.**
- `__Secure-` — the cookie must be set with `Secure`. Use only when subdomain sharing is req...
- [Session_Management_Cheat_Sheet:018] Session Management Cheat Sheet > Cookies > Domain and Path Attributes: The `Domain` cookie attribute instructs web browsers to only send the cookie to the specified domain and all subdomains. If the attribute is not set, by default the cookie will only be sent to the origin server. The `Path` cookie attribute instructs web browsers to only send the cookie to the specified directory or subdirectories (or paths or resources) within the web application. If the attribute...
- [Session_Management_Cheat_Sheet:014] Session Management Cheat Sheet > Cookies > Secure Attribute: The session ID exchange mechanism based on cookies provides multiple security features in the form of cookie attributes that can be used to protect the exchange of the session ID:

The `Secure` cookie attribute instructs web browsers to only send the cookie through an encrypted HTTPS (SSL/TLS) connection. This session protection mechanism is mandatory to prevent the disclosure of the session ID th...

## q07 (single)
**Question:** Can I store a JWT or refresh token in localStorage?
**Reference:** No: any JavaScript in the origin can read it, so one XSS leaks every token. Use HttpOnly; Secure; SameSite=Strict cookies or a Backend-for-Frontend.
**Answer:** No, you should not store authentication tokens, session IDs, JWTs, or refresh tokens in `localStorage` or `sessionStorage` [Session_Management_Cheat_Sheet:021]. 

These APIs are accessible to any JavaScript executing in the origin, meaning a single Cross-Site Scripting (XSS) vulnerability will disclose every stored token [Session_Management_Cheat_Sheet:021]. Instead, prefer `HttpOnly; Secure; SameSite=Strict` cookies or a Backend-for-Frontend (BFF) pattern [Session_Management_Cheat_Sheet:021].
**Retrieved passages:**
- [Session_Management_Cheat_Sheet:021] Session Management Cheat Sheet > HTML5 Web Storage API > The localStorage API: The Web Hypertext Application Technology Working Group (WHATWG) describes the HTML5 Web Storage APIs, `localStorage` and `sessionStorage`, as mechanisms for storing name-value pairs client-side.
Unlike HTTP cookies, the contents of `localStorage` and `sessionStorage` are not automatically shared within requests or responses by the browser and are used for storing data client-side.

> [!WARNING]
> ...
- [Session_Management_Cheat_Sheet:022] Session Management Cheat Sheet > HTML5 Web Storage API > The localStorage API > Scope: Data stored using the `localStorage` API is accessible by pages which are loaded from the same origin, which is defined as the scheme (`https://`), host (`example.com`), port (`443`) and domain/realm (`example.com`).
This provides similar access to this data as would be achieved by using the `secure` flag on a cookie, meaning that data stored from `https` could not be retrieved via `http`. Due to ...
- [Session_Management_Cheat_Sheet:023] Session Management Cheat Sheet > HTML5 Web Storage API > The localStorage API > Use Case: Data stored using the `localStorage` API is persisted across browsing sessions, extending the timeframe in which it may be accessible to other system users.

The standards do not require `localStorage` data to be encrypted-at-rest, meaning it may be possible to directly access this data from disk.

WHATWG suggests the use of `localStorage` for data that needs to be accessed across windows or tabs,...
- [Forgot_Password_Cheat_Sheet:006] Forgot Password Cheat Sheet > Methods > General Security Practices: It is essential to employ good security practices for the reset identifiers (tokens, codes, PINs, etc.). Some points don't apply to the offline methods, such as the lifetime restriction. All tokens and codes should be:

- Generated using a cryptographically secure random number generator.
    - It is also possible to use JSON Web Tokens (JWTs) in place of random tokens, although this can introduce...
- [Session_Management_Cheat_Sheet:027] Session Management Cheat Sheet > Web Workers > Use Case: A worker can keep a secret in memory when persistence across page refresh is not required. To isolate the secret from the main window, obtain it within the worker, keep secret-dependent operations there, and never return the secret to the main window.

This isolation can reduce direct access to an existing secret, but it does not make the application safe against XSS. Malicious page code can still...

## q08 (single)
**Question:** Should my forgot-password form tell the user whether the email address has an account?
**Reference:** No: return the same message for existing and non-existing accounts, in a consistent time, and rate-limit requests.
**Answer:** No. You should return a consistent, generic message for both existent and non-existent accounts to prevent user enumeration attacks [Forgot_Password_Cheat_Sheet:001, Forgot_Password_Cheat_Sheet:002]. 

A correct response example is: "If that email address is in our database, we will send you an email to reset your password" [Authentication_Cheat_Sheet:018].
**Retrieved passages:**
- [Forgot_Password_Cheat_Sheet:001] Forgot Password Cheat Sheet > Introduction: In order to implement a proper user management system, systems integrate a **Forgot Password** service that allows the user to request a password reset.

Even though this functionality looks straightforward and easy to implement, it is a common source of vulnerabilities, such as the renowned user enumeration attack.

The following short guidelines can be used as a quick reference to protect the fo...
- [Forgot_Password_Cheat_Sheet:002] Forgot Password Cheat Sheet > Forgot Password Service > Forgot Password Request: The password reset process can be broken into two main steps, detailed in the following sections.

When a user uses the forgot password service and inputs their username or email, the below should be followed to implement a secure process:

- Return a consistent message for both existent and non-existent accounts.
- Ensure that responses return in a consistent amount of time to prevent an attacker...
- [Authentication_Cheat_Sheet:016] Authentication Cheat Sheet > Authentication General Guidelines > Authentication and Error Messages > Authentication Responses: Incorrectly implemented error messages in the case of authentication functionality can be used for the purposes of user ID and password enumeration. An application should respond (both HTTP and HTML) in a generic manner.

Using any of the authentication mechanisms (login, password reset, or password recovery), an application must respond with a generic error message regardless of whether:

- The u...
- [Authentication_Cheat_Sheet:018] Authentication Cheat Sheet > Authentication General Guidelines > Authentication and Error Messages > Authentication Responses > Incorrect and correct response examples > Password recovery: Incorrect response examples:

- "Login for User foo: invalid password."
- "Login failed, invalid user ID."
- "Login failed; account disabled."
- "Login failed; this user is not active."

Correct response example:

- "Login failed; Invalid user ID or password."

Incorrect response examples:

- "We just sent you a password reset link."
- "This email address doesn't exist in our database."

Correct r...
- [Forgot_Password_Cheat_Sheet:005] Forgot Password Cheat Sheet > Methods: In order to allow a user to request a password reset, you will need to have some way to identify the user, or a means to reach out to them through a side-channel.

This can be done through any of the following methods:

- URL tokens.
- PINs
- Offline methods
- Security questions.

These methods can be used together to provide a greater degree of assurance that the user is who they claim to be. No ...

## q09 (single)
**Question:** Which Referrer-Policy should the password reset page set?
**Reference:** no-referrer, to avoid leaking the reset token through the Referer header.
**Answer:** The password reset page should add the Referrer Policy tag with the `no-referrer` value in order to avoid referrer leakage (especially when URL tokens are used) [Forgot_Password_Cheat_Sheet:007].

> `Referrer-Policy: no-referrer`
**Retrieved passages:**
- [HTTP_Headers_Cheat_Sheet:004] HTTP Security Response Headers Cheat Sheet > Security Headers > Referrer-Policy > Recommendation: Set the Content-Type header correctly throughout the site.

> `X-Content-Type-Options: nosniff`

The `Referrer-Policy` HTTP header controls how much referrer information (sent via the Referer header) should be included with requests.

Modern browsers default to `strict-origin-when-cross-origin`: same-origin requests include the origin, path, and query string in the `Referer` header; cross-origin r...
- [Forgot_Password_Cheat_Sheet:007] Forgot Password Cheat Sheet > Methods > URL Tokens: URL tokens are passed in the query string of the URL, and are typically sent to the user via email. The basic overview of the process is as follows:

1. Generate a token for the user and attach it in the URL query string.
2. Send this token to the user via email.
   - Don't rely on the Host header while creating the reset URLs to avoid Host Header Injection attacks. The URL should either be hard-c...
- [Forgot_Password_Cheat_Sheet:001] Forgot Password Cheat Sheet > Introduction: In order to implement a proper user management system, systems integrate a **Forgot Password** service that allows the user to request a password reset.

Even though this functionality looks straightforward and easy to implement, it is a common source of vulnerabilities, such as the renowned user enumeration attack.

The following short guidelines can be used as a quick reference to protect the fo...
- [Forgot_Password_Cheat_Sheet:003] Forgot Password Cheat Sheet > Forgot Password Service > User Resets Password: Once the user has proved their identity by providing the token (sent via an email) or code (sent via SMS or other mechanisms), they should reset their password to a new secure one. In order to secure this step, the measures that should be taken are:

- The user should confirm the password they set by writing it twice.
- Ensure that a secure password policy is in place, and is consistent with the r...
- [Forgot_Password_Cheat_Sheet:006] Forgot Password Cheat Sheet > Methods > General Security Practices: It is essential to employ good security practices for the reset identifiers (tokens, codes, PINs, etc.). Some points don't apply to the offline methods, such as the lifetime restriction. All tokens and codes should be:

- Generated using a cryptographically secure random number generator.
    - It is also possible to use JSON Web Tokens (JWTs) in place of random tokens, although this can introduce...

## q10 (single)
**Question:** Can I use security questions as the only way for users to reset their password?
**Reference:** No: answers are often guessable or obtainable; use them only as an additional layer with other methods.
**Answer:** No, security questions should not be used as the sole mechanism for resetting passwords because their answers are frequently easily guessable or obtainable by attackers [Forgot_Password_Cheat_Sheet:010]. They can instead be used as an additional layer of security when combined with other methods [Forgot_Password_Cheat_Sheet:010].
**Retrieved passages:**
- [Forgot_Password_Cheat_Sheet:005] Forgot Password Cheat Sheet > Methods: In order to allow a user to request a password reset, you will need to have some way to identify the user, or a means to reach out to them through a side-channel.

This can be done through any of the following methods:

- URL tokens.
- PINs
- Offline methods
- Security questions.

These methods can be used together to provide a greater degree of assurance that the user is who they claim to be. No ...
- [Forgot_Password_Cheat_Sheet:010] Forgot Password Cheat Sheet > Methods > Security Questions: Security questions should not be used as the sole mechanism for resetting passwords due to their answers frequently being easily guessable or obtainable by attackers. However, they can provide an additional layer of security when combined with the other methods discussed in this cheat sheet. If they are used, then ensure that secure questions are chosen as discussed in the Security Questions cheat...
- [Forgot_Password_Cheat_Sheet:003] Forgot Password Cheat Sheet > Forgot Password Service > User Resets Password: Once the user has proved their identity by providing the token (sent via an email) or code (sent via SMS or other mechanisms), they should reset their password to a new secure one. In order to secure this step, the measures that should be taken are:

- The user should confirm the password they set by writing it twice.
- Ensure that a secure password policy is in place, and is consistent with the r...
- [Multifactor_Authentication_Cheat_Sheet:017] Multifactor Authentication Cheat Sheet > Something You Know > Security Questions: - Simple and well understood.
- Native support in every authentication framework.
- Easy to implement.

- Users are prone to choosing weak passwords.
- Passwords are commonly re-used between systems.
- Susceptible to phishing.

**Security questions are no longer recognized as an acceptable authentication factor** per NIST SP 800-63. Account recovery is just an alternate way to authenticate so it s...
- [Forgot_Password_Cheat_Sheet:002] Forgot Password Cheat Sheet > Forgot Password Service > Forgot Password Request: The password reset process can be broken into two main steps, detailed in the following sections.

When a user uses the forgot password service and inputs their username or email, the below should be followed to implement a secure process:

- Return a consistent message for both existent and non-existent accounts.
- Ensure that responses return in a consistent amount of time to prevent an attacker...

## q11 (single)
**Question:** Is it worth hashing one-time passcodes before storing them?
**Reference:** Yes, but only for short-term exposure protection (logs, brief database exposure): a 6-digit OTP has about a million values, so hashing gives no strong offline resistance.
**Answer:** Yes, hashing server-generated one-time passcodes (OTPs) is still recommended, but keep in mind its limitations:

* **It does not provide strong offline resistance:** Because OTPs have a very small keyspace (e.g., about one million possibilities for a 6-digit code), a database attacker can quickly brute-force any OTP hash [Multifactor_Authentication_Cheat_Sheet:008].
* **It protects against short-term exposure:** Hashing prevents accidental disclosure through logs, metrics, or debugging tools, reduces the blast radius if the database is briefly exposed during the OTP's validity window, and enforces good secret-handling discipline by avoiding plaintext storage by default [Multifactor_Authentication_Cheat_Sheet:008]. 

The goal of hashing OTPs is short-term exposure protection, not long-term cryptographic secrecy [Multifactor_Authentication_Cheat_Sheet:008].
**Retrieved passages:**
- [Multifactor_Authentication_Cheat_Sheet:008] Multifactor Authentication Cheat Sheet > Implementing MFA > One-Time Password (OTP) Handling and Storage > Hashing OTPs: Hashing OTPs is still recommended, but for different reasons than password hashing. OTPs typically have a very small keyspace (for example, ~1 million possibilities for a 6-digit code), which means a database attacker can brute-force any OTP hash quickly.

As a result, hashing OTPs does not provide strong offline attack resistance in the way password hashing does.

However, hashing remains useful ...
- [Multifactor_Authentication_Cheat_Sheet:007] Multifactor Authentication Cheat Sheet > Implementing MFA > One-Time Password (OTP) Handling and Storage: OTPs are authentication secrets and should be handled with password-like hygiene. While their security traits differ from long-lived passwords, improper handling can still lead to user account compromise.

At a minimum, OTP implementations SHOULD:

- Enforce a short time-to-live (TTL)
- Ensure OTPs are single use
- Apply strict attempt limits
- Invalidate the OTP on successful verification

OTP im...
- [Multifactor_Authentication_Cheat_Sheet:009] Multifactor Authentication Cheat Sheet > Implementing MFA > One-Time Password (OTP) Handling and Storage > TOTP Seeds and Validation Window: The storage guidance above is for OTPs the server generates and sends. With TOTP the server instead keeps a long-lived shared seed and computes the expected codes from it, so the seed can't be hashed, and anyone who obtains it can generate valid codes until the user enrolls a new one. Strict attempt limits still apply to TOTP verification.

- Store TOTP seeds encrypted, ideally with a key held in ...
- [Multifactor_Authentication_Cheat_Sheet:021] Multifactor Authentication Cheat Sheet > Something You Have > One-Time Password Tokens > Software OTP Tokens: A cheaper and easier alternative to hardware tokens is using software to generate Time-based One-Time Password (TOTP) codes. This would typically involve the user installing a TOTP application on their mobile phone, and then scanning a QR code provided by the web application which provides the initial seed. The authenticator app generates a numeric code using a configured time step; RFC 6238 recom...
- [Session_Management_Cheat_Sheet:010] Session Management Cheat Sheet > Session Management Implementation > Server-Side Session Token Storage: Storing random session tokens verbatim can be acceptable in a tightly controlled session store, but anyone who can read it can reuse unexpired tokens. High entropy protects against guessing; it does not protect exposed tokens. If read-only disclosure of the store is in your threat model, store a one-way verifier instead. RFC 6819 recommends token hashes for the corresponding OAuth access-token dat...

## q12 (single)
**Question:** How should I store the TOTP seeds of my users?
**Reference:** Encrypted, ideally with a key in an HSM or KMS, decrypted only while verifying a code, and never returned to the client after enrollment.
**Answer:** To securely store user TOTP seeds:

* Store TOTP seeds encrypted, ideally using a key managed by a key management service (KMS) or held in a hardware security module (HSM) [Multifactor_Authentication_Cheat_Sheet:009].
* Decrypt the seed only while verifying a code [Multifactor_Authentication_Cheat_Sheet:009].
* Never return the seed to the client after initial enrollment [Multifactor_Authentication_Cheat_Sheet:009].
**Retrieved passages:**
- [Multifactor_Authentication_Cheat_Sheet:009] Multifactor Authentication Cheat Sheet > Implementing MFA > One-Time Password (OTP) Handling and Storage > TOTP Seeds and Validation Window: The storage guidance above is for OTPs the server generates and sends. With TOTP the server instead keeps a long-lived shared seed and computes the expected codes from it, so the seed can't be hashed, and anyone who obtains it can generate valid codes until the user enrolls a new one. Strict attempt limits still apply to TOTP verification.

- Store TOTP seeds encrypted, ideally with a key held in ...
- [Multifactor_Authentication_Cheat_Sheet:021] Multifactor Authentication Cheat Sheet > Something You Have > One-Time Password Tokens > Software OTP Tokens: A cheaper and easier alternative to hardware tokens is using software to generate Time-based One-Time Password (TOTP) codes. This would typically involve the user installing a TOTP application on their mobile phone, and then scanning a QR code provided by the web application which provides the initial seed. The authenticator app generates a numeric code using a configured time step; RFC 6238 recom...
- [Multifactor_Authentication_Cheat_Sheet:007] Multifactor Authentication Cheat Sheet > Implementing MFA > One-Time Password (OTP) Handling and Storage: OTPs are authentication secrets and should be handled with password-like hygiene. While their security traits differ from long-lived passwords, improper handling can still lead to user account compromise.

At a minimum, OTP implementations SHOULD:

- Enforce a short time-to-live (TTL)
- Ensure OTPs are single use
- Apply strict attempt limits
- Invalidate the OTP on successful verification

OTP im...
- [Multifactor_Authentication_Cheat_Sheet:004] Multifactor Authentication Cheat Sheet > Quick Recommendations: Exactly when and how MFA is implemented in an application will vary on a number of different factors, including the threat model of the application, the technical level of the users, and the level of administrative control over the users. These need to be considered on a per-application basis.

However, the following recommendations are generally appropriate for most applications, and provide an i...
- [Multifactor_Authentication_Cheat_Sheet:022] Multifactor Authentication Cheat Sheet > Something You Have > One-Time Password Tokens > Software OTP Tokens > Pros: - The absence of physical tokens greatly reduces the cost and administrative overhead of implementing the system.
- When users lose access to their TOTP app, a new one can be configured without needing to ship a physical token to them.
- TOTP is widely used, and many users will already have at least one TOTP app installed.
- A screen lock reduces theft risk but does not guarantee protection if the...

## q13 (single)
**Question:** Is SMS an acceptable second factor for an online banking app?
**Reference:** No: SMS is a restricted authenticator (SIM swap, SS7 interception) and should not protect applications with PII or financial risk.
**Answer:** No, SMS is not an acceptable second factor for an online banking app [Multifactor_Authentication_Cheat_Sheet:028]. 

SMS and PSTN-delivered codes are designated as restricted authenticators because they are susceptible to SIM-swapping, number-porting, SS7 interception, and phishing attacks [Multifactor_Authentication_Cheat_Sheet:028, Multifactor_Authentication_Cheat_Sheet:029]. They should not be used to protect applications that involve financial risk or hold Personally Identifiable Information (PII) [Multifactor_Authentication_Cheat_Sheet:028].
**Retrieved passages:**
- [Multifactor_Authentication_Cheat_Sheet:028] Multifactor Authentication Cheat Sheet > Something You Have > SMS Messages and Phone Calls: > [!WARNING]
> NIST SP 800-63B-4 designates SMS and PSTN-delivered codes as a *restricted* authenticator because of SS7 interception, SIM-swap, and number-porting attacks. Do not use SMS for high-value or PII-handling applications. Where it is the only available factor, document the risk acceptance, enforce per-account rate limits, monitor for SIM-swap signals, and plan migration to TOTP, push not...
- [Multifactor_Authentication_Cheat_Sheet:029] Multifactor Authentication Cheat Sheet > Something You Have > SMS Messages and Phone Calls > Cons: - Relatively simple to implement.
- Requires user to link their account to a mobile number.

- Requires the user to have a mobile device or landline.
- Require user to have signal or internet access to receive the call or message.
- Calls and SMS messages may cost money to send need to protect against attackers requesting a large number of messages to exhaust funds.
- Susceptible to SIM swapping a...
- [Multifactor_Authentication_Cheat_Sheet:004] Multifactor Authentication Cheat Sheet > Quick Recommendations: Exactly when and how MFA is implemented in an application will vary on a number of different factors, including the threat model of the application, the technical level of the users, and the level of administrative control over the users. These need to be considered on a per-application basis.

However, the following recommendations are generally appropriate for most applications, and provide an i...
- [Multifactor_Authentication_Cheat_Sheet:001] Multifactor Authentication Cheat Sheet > Introduction: Multifactor Authentication (MFA) requires evidence from at least two distinct authentication factors: something you know, something you have, and something you are. Location and other risk signals can inform authentication decisions, but do not substitute for an authentication factor, as explained in NIST SP 800-63B-4.

| Factor | Examples |
|--------|----------|
| Something You Know | Passwords a...
- [Multifactor_Authentication_Cheat_Sheet:030] Multifactor Authentication Cheat Sheet > Something You Have > Email: Email verification requires that the user enters a code or clicks a link sent to their email address. There is some debate as to whether email constitutes a form of MFA, because if the user does not have MFA configured on their email account, it simply requires knowledge of the user's email password (which is often the same as their application password). However, it is included here for completen...

## q14 (single)
**Question:** What should my login page say when the username does not exist?
**Reference:** A generic error message, the same whether the user ID or password is wrong, the account does not exist, or it is locked, to prevent user enumeration.
**Answer:** Your login page should respond with a generic error message, such as "Login failed; Invalid user ID or password," regardless of whether the account exists, the password was incorrect, or the account is locked or disabled [Authentication_Cheat_Sheet:016, Authentication_Cheat_Sheet:018]. This prevents attackers from using user enumeration to discover valid usernames [Authentication_Cheat_Sheet:016].
**Retrieved passages:**
- [Authentication_Cheat_Sheet:016] Authentication Cheat Sheet > Authentication General Guidelines > Authentication and Error Messages > Authentication Responses: Incorrectly implemented error messages in the case of authentication functionality can be used for the purposes of user ID and password enumeration. An application should respond (both HTTP and HTML) in a generic manner.

Using any of the authentication mechanisms (login, password reset, or password recovery), an application must respond with a generic error message regardless of whether:

- The u...
- [Authentication_Cheat_Sheet:018] Authentication Cheat Sheet > Authentication General Guidelines > Authentication and Error Messages > Authentication Responses > Incorrect and correct response examples > Password recovery: Incorrect response examples:

- "Login for User foo: invalid password."
- "Login failed, invalid user ID."
- "Login failed; account disabled."
- "Login failed; this user is not active."

Correct response example:

- "Login failed; Invalid user ID or password."

Incorrect response examples:

- "We just sent you a password reset link."
- "This email address doesn't exist in our database."

Correct r...
- [Authentication_Cheat_Sheet:019] Authentication Cheat Sheet > Authentication General Guidelines > Authentication and Error Messages > Authentication Responses > Error Codes and URLs: Incorrect response examples:

- "This user ID is already in use."
- "Welcome! You have signed up successfully."

Correct response example:

- "A link to activate your account has been emailed to the address provided."

The application may return a different HTTP Error code depending on the authentication attempt response. It may respond with a 200 for a positive result and a 403 for a negative res...
- [Authentication_Cheat_Sheet:017] Authentication Cheat Sheet > Authentication General Guidelines > Authentication and Error Messages > Authentication Responses: - Second implementation without relying on the "quick exit" approach:

```text
password_hash=HASH(password)
IS_VALID=LOOKUP_CREDENTIALS_IN_STORE(username, password_hash)
IF NOT IS_VALID THEN
   RETURN Error("Invalid Username or Password!")
ENDIF
```

This code will go through the same process no matter what the user or the password is, allowing the application to return in approximately the same r...
- [Authentication_Cheat_Sheet:002] Authentication Cheat Sheet > Authentication General Guidelines > Usernames: The primary function of a User ID is to uniquely identify a user within a system. Ideally, User IDs should be randomly generated to prevent the creation of predictable or sequential IDs, which could pose a security risk, especially in systems where User IDs might be exposed or inferred from external sources.

Usernames are easy-to-remember identifiers chosen by the user and used for identifying th...

## q15 (single)
**Question:** Should I count failed login attempts per IP address or per account?
**Reference:** Per account, so an attacker cannot spread attempts over many IP addresses.
**Answer:** You should associate the counter of failed logins with the account itself rather than the source IP address [Authentication_Cheat_Sheet:022]. This prevents an attacker from bypassing the protection by making login attempts from a large number of different IP addresses [Authentication_Cheat_Sheet:022].
**Retrieved passages:**
- [Authentication_Cheat_Sheet:022] Authentication Cheat Sheet > Authentication General Guidelines > Protect Against Automated Attacks > Login Throttling > Account Lockout: Login Throttling is a security mechanism used to prevent an attacker from making too many attempts at guessing a password through normal interactive means, it includes the following controls:

- Maximum number of attempts.

The most common protection against these attacks is to implement account lockout, which prevents any more login attempts for a period after a certain number of failed logins.

...
- [Multifactor_Authentication_Cheat_Sheet:012] Multifactor Authentication Cheat Sheet > Implementing MFA > Failed Login Attempts: When a user enters their password, but fails to authenticate using a second factor, this could mean one of two things:

- The user has lost their second factor, or doesn't have it available (for example, they don't have their mobile phone, or have no signal).
- The user's password has been compromised.

There are a number of steps that should be taken when this occurs:

- Prompt the user to try an...
- [Authentication_Cheat_Sheet:024] Authentication Cheat Sheet > Logging and Monitoring: Do not use security questions for authentication or re-authentication; ASVS 6.4.2 excludes knowledge-based authentication. When verifying a password or memorable word, request and verify the full secret rather than selected characters, as required by NIST SP 800-63B-4. See the Choosing and Using Security Questions Cheat Sheet for guidance limited to legacy systems.

Enable logging and monitoring o...
- [Session_Management_Cheat_Sheet:048] Session Management Cheat Sheet > Session Attacks Detection > Simultaneous Session Logons: It is the web application design decision to determine if multiple simultaneous logons from the same user are allowed from the same or from different client IP addresses. If the web application does not want to allow simultaneous session logons, it must take effective actions after each new authentication event, implicitly terminating the previously available session, or asking the user (through t...
- [Session_Management_Cheat_Sheet:044] Session Management Cheat Sheet > Session Attacks Detection > Session ID Guessing and Brute Force Detection: If an attacker tries to guess or brute force a valid session ID, they need to launch multiple sequential requests against the target web application using different session IDs from a single (or set of) IP address(es). Additionally, if an attacker tries to analyze the predictability of the session ID (e.g. using statistical analysis), they need to launch multiple sequential requests from a single ...

## q16 (single)
**Question:** What file name should I use to store files that users upload?
**Reference:** A random string such as a UUID; if the original name is needed, validate it on the client and server.
**Answer:** You should create a **random string** as a filename, such as generating a UUID/GUID [File_Upload_Cheat_Sheet:007]. Generating the stored filename server-side removes risks associated with user-supplied filenames, including special files creation or overwrite attacks and Windows 8.3 short name collisions [File_Upload_Cheat_Sheet:007, File_Upload_Cheat_Sheet:008].

If business needs require using the user's original filename, implement proper input validation including:
- A maximum length limit [File_Upload_Cheat_Sheet:007]
- Restricting characters to an allowed subset specifically (such as alphanumeric characters, hyphen, spaces, and periods) [File_Upload_Cheat_Sheet:007]
- Restricting leading periods, sequential periods, leading hyphens, and leading spaces [File_Upload_Cheat_Sheet:007]
**Retrieved passages:**
- [File_Upload_Cheat_Sheet:007] File Upload Cheat Sheet > File Upload Protection > Filename Safety: In conjunction with content-type validation, validating the file's signature can be checked and verified against the expected file that should be received.

> This should not be used on its own, as bypassing it is pretty common and easy.

Filenames can endanger the system in multiple ways, either by using non acceptable characters, or by using special and restricted filenames. For Windows, refer t...
- [File_Upload_Cheat_Sheet:010] File Upload Cheat Sheet > File Upload Protection > File Storage Location: The location where the files should be stored must be chosen based on security and business requirements. The following points are set by security priority, and are inclusive:

1. Store the files on a **different host**, which allows for complete segregation of duties between the application serving the user, and the host handling file uploads and their storage.
2. Store the files **outside the we...
- [File_Upload_Cheat_Sheet:008] File Upload Cheat Sheet > File Upload Protection > Filename Safety: On Windows/NTFS, a long filename may have an 8.3 short name alias, depending on file system settings. Do not assume that an alias exists or has a particular spelling. If an overwrite or collision check validates only the long filename supplied by the user, an attacker who can predict the short alias of an existing sensitive file may reference it directly to overwrite that file, bypassing an exact-...
- [File_Upload_Cheat_Sheet:011] File Upload Cheat Sheet > File Upload Protection > File Storage Location: > Some files are emailed or processed once they are uploaded, and are not stored on the server. It is essential to conduct the security measures discussed in this sheet before doing any actions on them....
- [File_Upload_Cheat_Sheet:013] File Upload Cheat Sheet > File Upload Protection > Filesystem Permissions: > Set the files permissions on the principle of least privilege.

Files should be stored in a way that ensures:

- Allowed system users are the only ones capable of reading the files
- Required modes only are set for the file
    - If execution is required, scanning the file before running it is required as a security best practice, to ensure that no macros or hidden scripts are available....

## q17 (single)
**Question:** Where should uploaded files be stored?
**Reference:** Best on a different host; otherwise outside the webroot; at worst inside the webroot with write-only permissions.
**Answer:** Based on security priority, uploaded files should be stored using the following approaches (inclusive):

1. **On a different host**, allowing complete segregation of duties between the application serving the user and the host handling file uploads and storage [File_Upload_Cheat_Sheet:010, File_Upload_Cheat_Sheet:001].
2. **Outside the webroot**, where only administrative access is allowed [File_Upload_Cheat_Sheet:010].
3. If stored **inside the webroot**, set them to write permissions only, and apply proper access controls if read access is required [File_Upload_Cheat_Sheet:010].

Additionally, disable per-directory configuration overrides on upload directories at the web server level (such as Apache `AllowOverride None` or locked IIS handler mappings) to prevent attackers from uploading configuration files like `.htaccess` or `web.config` [File_Upload_Cheat_Sheet:010].
**Retrieved passages:**
- [File_Upload_Cheat_Sheet:010] File Upload Cheat Sheet > File Upload Protection > File Storage Location: The location where the files should be stored must be chosen based on security and business requirements. The following points are set by security priority, and are inclusive:

1. Store the files on a **different host**, which allows for complete segregation of duties between the application serving the user, and the host handling file uploads and their storage.
2. Store the files **outside the we...
- [File_Upload_Cheat_Sheet:013] File Upload Cheat Sheet > File Upload Protection > Filesystem Permissions: > Set the files permissions on the principle of least privilege.

Files should be stored in a way that ensures:

- Allowed system users are the only ones capable of reading the files
- Required modes only are set for the file
    - If execution is required, scanning the file before running it is required as a security best practice, to ensure that no macros or hidden scripts are available....
- [File_Upload_Cheat_Sheet:001] File Upload Cheat Sheet > Introduction: File upload is becoming a more and more essential part of any application, where the user is able to upload their photo, their CV, or a video showcasing a project they are working on. The application should be able to fend off bogus and malicious files in a way to keep the application and the users safe.

In short, the following principles should be followed to reach a secure file upload implement...
- [File_Upload_Cheat_Sheet:011] File Upload Cheat Sheet > File Upload Protection > File Storage Location: > Some files are emailed or processed once they are uploaded, and are not stored on the server. It is essential to conduct the security measures discussed in this sheet before doing any actions on them....
- [File_Upload_Cheat_Sheet:007] File Upload Cheat Sheet > File Upload Protection > Filename Safety: In conjunction with content-type validation, validating the file's signature can be checked and verified against the expected file that should be received.

> This should not be used on its own, as bypassing it is pretty common and easy.

Filenames can endanger the system in multiple ways, either by using non acceptable characters, or by using special and restricted filenames. For Windows, refer t...

## q18 (single)
**Question:** Is escaping user input enough to prevent SQL injection?
**Reference:** No, manual escaping is strongly discouraged as error-prone; use parameterized queries.
**Answer:** No, manually escaping untrusted values to construct SQL queries is strongly discouraged and is not enough to prevent SQL injection [SQL_Injection_Prevention_Cheat_Sheet:008]. 

Manual escaping is error-prone and can fail because:
- SQL escaping rules are not always straightforward [SQL_Injection_Prevention_Cheat_Sheet:008].
- Different SQL dialects have different rules [SQL_Injection_Prevention_Cheat_Sheet:008].
- Database configurations (such as MySQL `NO_BACKSLASH_ESCAPES`) can affect escaping behavior [SQL_Injection_Prevention_Cheat_Sheet:008].

Instead, you should use **parameterized queries** (parameter binding) to separate the SQL structure from its data values [SQL_Injection_Prevention_Cheat_Sheet:001, SQL_Injection_Prevention_Cheat_Sheet:006].
**Retrieved passages:**
- [SQL_Injection_Prevention_Cheat_Sheet:008] SQL Injection Prevention Cheat Sheet > Primary Defenses > Manually escaping (STRONGLY DISCOURAGED): **Do not manually escape untrusted values to construct SQL queries. Use parameterized queries instead.**

Manually escaping the values into the SQL string is error-prone and attempts to do something which is normally handled by the database driver through parameter bindings. It can fail and can allow SQL injections for several reasons:

- SQL escaping rules are not always straightforward;
- differ...
- [SQL_Injection_Prevention_Cheat_Sheet:006] SQL Injection Prevention Cheat Sheet > Primary Defenses > Parameterized Queries: The preferred patterns are:

- **parameterized queries** when including dynamic data in SQL requests;
- for structural parts that cannot be parameterized (table names, column names, sort direction), map user choices to a **strict allow-list** of fixed, application-owned values.

Relying on manually escaping dynamic inputs is error-prone and is strongly discouraged.

Define the SQL structure separa...
- [SQL_Injection_Prevention_Cheat_Sheet:002] SQL Injection Prevention Cheat Sheet > Examples of injections > Basic SQL injection: A simple SQL injection flaw in Java is shown below. The "customerName" parameter is simply concatenated to build the query and an attacker can enter SQL code into that query and the application would take the attacker's code and execute it on the database.

```java
// UNSAFE!
String query = "SELECT account_balance FROM user_data WHERE user_name = '"
    + request.getParameter("customerName") + "'"...
- [SQL_Injection_Prevention_Cheat_Sheet:014] SQL Injection Prevention Cheat Sheet > Testing and detection: Input validation complements parameter binding; it does not replace it. Continue binding all data values, even when they pass type, length, or format checks. Validation of a value does not make it safe to concatenate into SQL, and a validation approach that is safe for one SQL dialect may be unsafe for another. See the Input Validation Cheat Sheet.

Review query construction in application code an...
- [SQL_Injection_Prevention_Cheat_Sheet:001] SQL Injection Prevention Cheat Sheet > Introduction: A SQL injection attack occurs when untrusted data (usually strings) becomes part of a query's SQL syntax, modifying the logic of the SQL request.

The malicious data can come from various sources such as:

- an HTTP request (for example, from a malicious user);
- an LDAP directory;
- an incoming email;
- a third party REST API service;
- the database itself.

**Impact:** A successful SQL injection...

## q19 (single)
**Question:** How can I safely let users choose which column to sort a SQL query by?
**Reference:** Map the user's choice to a strict allow-list of fixed, application-owned values, since column names cannot be parameterized.
**Answer:** Because parameter markers cannot represent column names or SQL keywords like `ASC` and `DESC`, you must map user choices to a strict allow-list of fixed, application-owned values rather than appending the supplied text directly [SQL_Injection_Prevention_Cheat_Sheet:007, SQL_Injection_Prevention_Cheat_Sheet:006]. 

Map the user's selection using a switch statement or map to select the allowed column name or sort direction, and reject anything else [SQL_Injection_Prevention_Cheat_Sheet:007]:

```java
String tableName;
switch(PARAM) {
  case "room":
    tableName = "roomTable";
    break;
  case "floor":
    tableName = "floorTable";
    break;
  default:
    throw new InputValidationException("unexpected table name");
}
```
**Retrieved passages:**
- [SQL_Injection_Prevention_Cheat_Sheet:007] SQL Injection Prevention Cheat Sheet > Primary Defenses > Allow-List Input Validation: Parameter markers represent data values, not table names, column names, or SQL keywords such as `ASC` and `DESC`; see the PDO parameter-marker limitations. Keep these structural choices fixed in code where possible. When users need to select among them, map their selection to a small set of application-owned values allowed for that query and reject anything else. In this example, `tableName` can o...
- [SQL_Injection_Prevention_Cheat_Sheet:006] SQL Injection Prevention Cheat Sheet > Primary Defenses > Parameterized Queries: The preferred patterns are:

- **parameterized queries** when including dynamic data in SQL requests;
- for structural parts that cannot be parameterized (table names, column names, sort direction), map user choices to a **strict allow-list** of fixed, application-owned values.

Relying on manually escaping dynamic inputs is error-prone and is strongly discouraged.

Define the SQL structure separa...
- [SQL_Injection_Prevention_Cheat_Sheet:001] SQL Injection Prevention Cheat Sheet > Introduction: A SQL injection attack occurs when untrusted data (usually strings) becomes part of a query's SQL syntax, modifying the logic of the SQL request.

The malicious data can come from various sources such as:

- an HTTP request (for example, from a malicious user);
- an LDAP directory;
- an incoming email;
- a third party REST API service;
- the database itself.

**Impact:** A successful SQL injection...
- [SQL_Injection_Prevention_Cheat_Sheet:014] SQL Injection Prevention Cheat Sheet > Testing and detection: Input validation complements parameter binding; it does not replace it. Continue binding all data values, even when they pass type, length, or format checks. Validation of a value does not make it safe to concatenate into SQL, and a validation approach that is safe for one SQL dialect may be unsafe for another. See the Input Validation Cheat Sheet.

Review query construction in application code an...
- [SQL_Injection_Prevention_Cheat_Sheet:005] SQL Injection Prevention Cheat Sheet > Examples of injections > SQL Injection inside stored Procedures and Functions: **Binding procedure arguments protects the call, not dynamic SQL constructed inside the procedure.**

Use static SQL with parameters, or separately bind data values in internal dynamic queries instead of concatenating them into SQL text. Microsoft's secure dynamic SQL guidance calls for reviewing procedures that construct SQL and parameterizing their commands.

For example, PostgreSQL documents `E...

## q20 (single)
**Question:** What value should I set for the Strict-Transport-Security header?
**Reference:** Strict-Transport-Security: max-age=63072000; includeSubDomains; preload (read how it works first: misconfiguration can lock users out).
**Answer:** Set the `Strict-Transport-Security` header to:

`Strict-Transport-Security: max-age=63072000; includeSubDomains; preload` [HTTP_Headers_Cheat_Sheet:008]

*Note:* Carefully check how HSTS works and review preload requirements before applying it, as misconfiguration or SSL/TLS certificate issues can lock users out of your site for the duration of the `max-age` [HTTP_Headers_Cheat_Sheet:008].
**Retrieved passages:**
- [HTTP_Headers_Cheat_Sheet:008] HTTP Security Response Headers Cheat Sheet > Security Headers > Strict-Transport-Security (HSTS) > Recommendation: The HTTP `Strict-Transport-Security` response header (often abbreviated as HSTS) instructs browsers to only access the website using HTTPS, even if a user attempts to connect over HTTP.

> `Strict-Transport-Security: max-age=63072000; includeSubDomains; preload`

- *NOTE*: Read carefully how this header works before using it. If the HSTS header is misconfigured or if there is a problem with the SS...
- [HTTP_Headers_Cheat_Sheet:006] HTTP Security Response Headers Cheat Sheet > Security Headers > Cache-Control > Recommendation: > `Content-Type: text/html; charset=UTF-8`

- *NOTE:* the `charset` attribute is necessary to prevent XSS in **HTML** pages
- *NOTE*: the `Content-Type` can be any of the possible MIME types

The `Cache-Control` header defines how responses are cached by browsers and intermediate caches.

- Use `no-store` for sensitive responses to prohibit storage in compliant HTTP caches.
- Use `private` to allo...
- [HTTP_Headers_Cheat_Sheet:004] HTTP Security Response Headers Cheat Sheet > Security Headers > Referrer-Policy > Recommendation: Set the Content-Type header correctly throughout the site.

> `X-Content-Type-Options: nosniff`

The `Referrer-Policy` HTTP header controls how much referrer information (sent via the Referer header) should be included with requests.

Modern browsers default to `strict-origin-when-cross-origin`: same-origin requests include the origin, path, and query string in the `Referer` header; cross-origin r...
- [Content_Security_Policy_Cheat_Sheet:019] Content Security Policy Cheat Sheet > CSP Sample Policies > Strict Policy: A strict policy's role is to protect against classical stored, reflected, and some of the DOM XSS attacks and should be the optimal goal of any team trying to implement CSP.

As noted above, Google went ahead and set up a detailed and methodological instructions for creating a Strict CSP.

Based on those instructions, one of the following two policies can be used to apply a strict policy:...
- [Session_Management_Cheat_Sheet:012] Session Management Cheat Sheet > Session Management Implementation > Transport Layer Security: In order to protect the session ID exchange from active eavesdropping and passive disclosure in the network traffic, it is essential to use an encrypted HTTPS (TLS) connection for the entire web session, not only for the authentication process where the user credentials are exchanged. This may be mitigated by HTTP Strict Transport Security (HSTS) for a client that supports it.

Additionally, the `...

## q21 (single)
**Question:** Which data should never be written directly to application logs?
**Reference:** Among others: session IDs, access tokens, passwords, connection strings, encryption keys, sensitive PII and payment data, and source code; remove, mask, hash or encrypt them.
**Answer:** The following should usually not be recorded directly in application logs, and instead should be removed, masked, sanitized, hashed, or encrypted:

- Application source code [Logging_Cheat_Sheet:011]
- Session identification values (consider replacing with a hashed value if needed to track session-specific events) [Logging_Cheat_Sheet:011]
- Access tokens [Logging_Cheat_Sheet:011]
- Sensitive personal data and some forms of personally identifiable information (PII) such as health data, government identifiers, and data concerning vulnerable people [Logging_Cheat_Sheet:011]
- Authentication passwords [Logging_Cheat_Sheet:011]
- Database connection strings [Logging_Cheat_Sheet:011]
- Encryption keys and other primary secrets [Logging_Cheat_Sheet:011]
- Bank account or payment card holder data [Logging_Cheat_Sheet:011]
- Data of a higher security classification than the logging system is allowed to store [Logging_Cheat_Sheet:011]
- Commercially-sensitive information [Logging_Cheat_Sheet:011]
- Information it is illegal to collect in the relevant jurisdictions [Logging_Cheat_Sheet:011]
- Information a user has opted out of collecting, or has not consented to (e.g., "do not track" preferences or expired consent) [Logging_Cheat_Sheet:011]
**Retrieved passages:**
- [Logging_Cheat_Sheet:011] Logging Cheat Sheet > Design, implementation, and testing > Data to exclude: Never log data unless it is legally sanctioned. For example, intercepting some communications, monitoring employees, and collecting some data without consent may all be illegal.

Never exclude any events from "known" users such as other internal systems, "trusted" third parties, search engine robots, uptime/process and other remote monitoring systems, pen testers, auditors. However, you may want t...
- [Logging_Cheat_Sheet:012] Logging Cheat Sheet > Design, implementation, and testing > Data to exclude: In some systems, sanitization can be undertaken post log collection, and prior to log display....
- [Logging_Cheat_Sheet:006] Logging Cheat Sheet > Design, implementation, and testing > Which events to log: - Input validation failures e.g. protocol violations, unacceptable encodings, invalid parameter names and values
    - Log failures to validate a value against a discrete and finite list of valid values (e.g. a country from a dropdown), such as `input_validation_fail[:field,userid]`. Treat these as suspicious events, not proof of an attack: unexpected input can also result from misuse or client de...
- [Logging_Cheat_Sheet:007] Logging Cheat Sheet > Design, implementation, and testing > Which events to log: Optionally consider if the following events can be logged and whether it is desirable information:

- Sequencing failure
- Excessive use
- Data changes
- Fraud and other criminal activities
- Suspicious, unacceptable, or unexpected behavior
- Modifications to configuration
- Application code file and/or memory changes...
- [Logging_Cheat_Sheet:019] Logging Cheat Sheet > Deployment and operation > Protection: The logging mechanisms and collected event data must be protected from mis-use such as tampering in transit, and unauthorized access, modification and deletion once stored. Logs may contain personal and other sensitive information, or the data may contain information regarding the application's code and logic.

In addition, the collected information in the logs may itself have business value (to c...

## q22 (single)
**Question:** Which Fetch Metadata request header is the main signal for CSRF protection?
**Reference:** Sec-Fetch-Site; a fallback to standard origin verification is mandatory for browsers that do not send it.
**Answer:** The main signal for CSRF protection in Fetch Metadata request headers is **`Sec-Fetch-Site`** [Cross-Site_Request_Forgery_Prevention_Cheat_Sheet:010]. 

It indicates the relationship between the request initiator's origin and the target's origin (`same-origin`, `same-site`, `cross-site`, or `none`), making it the primary and most useful header for blocking untrusted cross-site requests [Cross-Site_Request_Forgery_Prevention_Cheat_Sheet:010, Cross-Site_Request_Forgery_Prevention_Cheat_Sheet:012].
**Retrieved passages:**
- [Cross-Site_Request_Forgery_Prevention_Cheat_Sheet:010] Cross-Site Request Forgery Prevention Cheat Sheet > Fetch Metadata headers: Fetch Metadata request headers provide extra information about the context from which an HTTP request was made. Servers can use these headers — most importantly `Sec-Fetch-Site` — as a lightweight and reliable method to block obvious cross-site requests. See the Fetch Metadata specification for details.

Because some legacy browsers do not send `Sec-Fetch-*` headers, a fallback to standard origin ...
- [Cross-Site_Request_Forgery_Prevention_Cheat_Sheet:014] Cross-Site Request Forgery Prevention Cheat Sheet > Fetch Metadata headers > Requirements: - Your application must be served over trustworthy URLs. Fetch Metadata request headers are only sent to potentially trustworthy URLs. In practice, this includes `https`, `wss`, `file`, and `localhost` (including `127.0.0.0/8` and `::1/128`). See the W3C Secure Contexts spec for full details.
- HTTPS must be enforced across the entire application. This ensures consistent inclusion of Fetch Metadat...
- [Cross-Site_Request_Forgery_Prevention_Cheat_Sheet:016] Cross-Site Request Forgery Prevention Cheat Sheet > Fetch Metadata headers > Rollout & testing recommendations: - Include an appropriate `Vary` header, in order to ensure that caches handle the response appropriately. For example, `Vary: Sec-Fetch-Site, Origin`. See more Fetch Metadata specification.
    - Note that the `Vary` header does not impact CSRF defenses in any way. It is a response header, so it is applied after the server has already made its allow/deny decision based on CSRF protections. Its pur...
- [Cross-Site_Request_Forgery_Prevention_Cheat_Sheet:012] Cross-Site Request Forgery Prevention Cheat Sheet > Fetch Metadata headers > How to treat Fetch Metadata headers on the server-side: `Sec-Fetch-Site` is the most useful Fetch Metadata header for blocking CSRF-like cross-origin requests and should be the primary signal in a Fetch-Metadata-based policy. Use other Fetch Metadata headers (`Sec-Fetch-Mode`, `Sec-Fetch-Dest`, `Sec-Fetch-User`) to further refine or tailor policies to your application's needs (for example, allowing top-level navigation requests or permitting specific D...
- [Cross-Site_Request_Forgery_Prevention_Cheat_Sheet:037] Cross-Site Request Forgery Prevention Cheat Sheet > JavaScript: Automatically Including CSRF Tokens as an AJAX Request Header: JavaScript clients can send CSRF tokens in a custom request header on protected state-changing requests. Prefer maintained framework or HTTP client integrations where available. Do not add CSRF tokens through global header defaults or by globally overriding `XMLHttpRequest.prototype.open`, because unrelated requests could receive the token.

Client-side CSRF handling does not replace server-side t...

## q23 (multi)
**Question:** I am replacing old MD5 password hashes: how should I migrate users, and which algorithm and settings should the new hashes use?
**Reference:** Re-hash with the new algorithm when users log in (and expire or reset long-inactive accounts); use Argon2id with a minimum configuration such as m=19 MiB, t=2, p=1.
**Answer:** ### Algorithm and Settings
Use a strong, slow hashing algorithm with a unique salt [Password_Storage_Cheat_Sheet:001]. Preferred choices and their minimum configurations are:
* **Argon2id** (recommended): Minimum configuration of 19 MiB of memory, an iteration count of 2, and 1 degree of parallelism [Password_Storage_Cheat_Sheet:001].
* **scrypt** (if Argon2id is unavailable): Minimum CPU/memory cost parameter of $2^{17}$, block size of 8 (1024 bytes), and parallelization parameter of 1 [Password_Storage_Cheat_Sheet:001].
* **bcrypt** (for legacy systems): Work factor of 10 or more (with a password limit of 72 bytes) [Password_Storage_Cheat_Sheet:001].
* **PBKDF2** (if FIPS-140 compliance is required): 600,000 or more iterations using HMAC-SHA-256 [Password_Storage_Cheat_Sheet:001].

Store the algorithm and work factor with the password using a standard format (such as the modular PHC string format) to easily allow a mix of old and new algorithms during the transition [Password_Storage_Cheat_Sheet:017].

---

### Migration Methods
When users authenticate, re-hash their plaintext password input using the new algorithm and replace the old hash [Password_Storage_Cheat_Sheet:016]. To handle users who have not logged in, choose one of two approaches:

1. **Upgrade Method One:** Expire and delete the password hashes of inactive users, requiring them to reset their passwords upon their next login (more secure, but less user-friendly) [Password_Storage_Cheat_Sheet:016].
2. **Upgrade Method Two:** Layer the old hash into the new algorithm temporarily (e.g., upgrading `md5($password)` to `bcrypt(md5($password))`), then replace it with a direct hash of the user's password the next time they log in [Password_Storage_Cheat_Sheet:016].
**Retrieved passages:**
- [Password_Storage_Cheat_Sheet:016] Password Storage Cheat Sheet > Upgrading Legacy Hashes: Older applications that use less secure hashing algorithms, such as MD5 or SHA-1, can be upgraded to modern password hashing algorithms as described above. When the users enter their password (usually by authenticating on the application), that input should be re-hashed using the new algorithm. Defenders should expire the users' current password and require them to enter a new one, so that any old...
- [Password_Storage_Cheat_Sheet:017] Password Storage Cheat Sheet > Upgrading Legacy Hashes: Remember that once your password hashing method is selected, it will have to be upgraded in the future, so ensure that upgrading your hashing algorithm is as easy as possible. During the transition period, allow for a mix of old and new hashing algorithms. Using a mix of hashing algorithms is easier if the password hashing algorithm and work factor are stored with the password using a standard for...
- [Password_Storage_Cheat_Sheet:009] Password Storage Cheat Sheet > Password Hashing Algorithms: Some modern hashing algorithms have been specifically designed to securely store passwords. This means that they should be slow (unlike algorithms such as MD5 and SHA-1, which were designed to be fast), and you can change how slow they are by changing the work factor.

You do not need to hide which password hashing algorithm is used by an application. If you utilize a modern password hashing algor...
- [Password_Storage_Cheat_Sheet:001] Password Storage Cheat Sheet > Introduction: This cheat sheet advises you on the proper methods for storing passwords for authentication. When passwords are stored, they must be protected from an attacker even if the application or database is compromised. Fortunately, a majority of modern languages and frameworks provide built-in functionality to help store passwords safely.

Passwords should never be stored in plain text. Instead, they mus...
- [Password_Storage_Cheat_Sheet:014] Password Storage Cheat Sheet > Password Hashing Algorithms > PBKDF2: Since PBKDF2 is permitted by NIST SP 800-63B-4 and has FIPS-140 validated implementations, it should be the preferred algorithm when these are required.

The PBKDF2 algorithm requires that you select an internal hashing algorithm such as an HMAC or a variety of other hashing algorithms. HMAC-SHA-256 is widely supported and is recommended by NIST.

The work factor for PBKDF2 is implemented through ...

## q24 (multi)
**Question:** Is the SameSite cookie attribute enough to protect against CSRF, and which value should my session cookie use?
**Reference:** No, it is defense in depth and does not replace a CSRF defense; set SameSite=Strict (preferred) or Lax explicitly on the session cookie.
**Answer:** No, the `SameSite` attribute is not enough to protect against CSRF on its own for most applications; it should be treated as defense-in-depth rather than a replacement for a CSRF token [Session_Management_Cheat_Sheet:016, Cross-Site_Request_Forgery_Prevention_Cheat_Sheet:028]. 

Your session cookie should explicitly use **`SameSite=Strict`** (preferred) or **`SameSite=Lax`** [Session_Management_Cheat_Sheet:016]. Do not rely on the browser-default value [Session_Management_Cheat_Sheet:016].
**Retrieved passages:**
- [Session_Management_Cheat_Sheet:016] Session Management Cheat Sheet > Cookies > SameSite Attribute: The `SameSite` attribute controls whether browsers send a cookie with cross-site requests. `SameSite=Strict` excludes cross-site requests, while `SameSite=Lax` permits top-level cross-site navigations that use safe HTTP methods. Treat `SameSite` as defense in depth against CSRF, not as a replacement for a CSRF token. Session cookies must explicitly set `SameSite=Strict` (preferred) or `SameSite=La...
- [Cross-Site_Request_Forgery_Prevention_Cheat_Sheet:025] Cross-Site Request Forgery Prevention Cheat Sheet > Defense In Depth Techniques > SameSite (Cookie Attribute): `SameSite` is a cookie attribute that controls whether browsers send cookies with cross-site requests. It is defined in RFC6265bis and takes one of three values:

- `Strict` prevents cookies from being sent with cross-site requests, including top-level navigations from external links. This can disrupt legitimate navigation into an application.
- `Lax` sends cookies on cross-site top-level navigati...
- [Cross-Site_Request_Forgery_Prevention_Cheat_Sheet:027] Cross-Site Request Forgery Prevention Cheat Sheet > Defense In Depth Techniques > SameSite (Cookie Attribute) > Limitations of SameSite: - **`Lax` only blocks unsafe methods.** The default `Lax` behavior still allows the cookie on top-level navigations that use safe methods (`GET`, `HEAD`, `OPTIONS`, `TRACE`). If any state-changing operation in the application is reachable via a `GET` request, `SameSite=Lax` will not stop it. This is the single most common way `SameSite`-based defenses fail in practice. Review every `GET` endpoint ...
- [Cross-Site_Request_Forgery_Prevention_Cheat_Sheet:028] Cross-Site Request Forgery Prevention Cheat Sheet > Defense In Depth Techniques > SameSite (Cookie Attribute) > Limitations of SameSite > When SameSite May Be Sufficient On Its Own: In narrow deployments `SameSite` alone can provide a reasonable CSRF defense, provided every one of the following holds:

- The application does not share a registrable domain with any host, subdomain, or service you do not fully control.
- No `GET` (or other safe-method) endpoint in the application performs a state-changing action. All state changes require `POST`, `PUT`, `PATCH`, or `DELETE`.
- ...
- [Cross-Site_Request_Forgery_Prevention_Cheat_Sheet:026] Cross-Site Request Forgery Prevention Cheat Sheet > Defense In Depth Techniques > SameSite (Cookie Attribute) > Limitations of SameSite: `SameSite` is useful as a defense-in-depth control but it does not replace a proper CSRF defense in most deployments. Treat the following as known gaps when reasoning about how much protection it actually provides:...

## q25 (multi)
**Question:** Should I use X-Frame-Options or Content Security Policy to stop my site being framed (clickjacking)?
**Reference:** CSP's frame-ancestors directive, which obsoletes X-Frame-Options in supporting browsers: frame-ancestors 'none' (or 'self' / a trusted domain).
**Answer:** You should use the Content Security Policy (CSP) `frame-ancestors` directive if possible, as it obsoletes `X-Frame-Options` for supporting browsers [HTTP_Headers_Cheat_Sheet:001, HTTP_Headers_Cheat_Sheet:002]. 

- Use CSP `frame-ancestors` to prevent framing attacks, for example:
  - To prevent all framing: `Content-Security-Policy: frame-ancestors 'none';` [Content_Security_Policy_Cheat_Sheet:021]
  - To allow only the site itself: `Content-Security-Policy: frame-ancestors 'self';` [Content_Security_Policy_Cheat_Sheet:021]
  - To allow a trusted domain: `Content-Security-Policy: frame-ancestors trusted.com;` [Content_Security_Policy_Cheat_Sheet:021]
**Retrieved passages:**
- [HTTP_Headers_Cheat_Sheet:001] HTTP Security Response Headers Cheat Sheet > Security Headers > X-Frame-Options: HTTP Headers are a great booster for web security with easy implementation. Proper HTTP response headers can help prevent security vulnerabilities like Cross-Site Scripting, Clickjacking, Information disclosure and more.

In this cheat sheet, we will review all security-related HTTP headers, recommended configurations, and reference other sources for complicated headers.

The `X-Frame-Options` HTT...
- [HTTP_Headers_Cheat_Sheet:002] HTTP Security Response Headers Cheat Sheet > Security Headers > X-XSS-Protection: Use Content Security Policy (CSP) frame-ancestors directive if possible.

Do not allow displaying of the page in a frame.
> `X-Frame-Options: DENY`

The HTTP `X-XSS-Protection` response header is a feature of Internet Explorer, Chrome, and Safari that stops pages from loading when they detect reflected cross-site scripting (XSS) attacks.

WARNING: Even though this header can protect users of older...
- [Content_Security_Policy_Cheat_Sheet:021] Content Security Policy Cheat Sheet > CSP Sample Policies > Preventing framing attacks (clickjacking, cross-site leaks): If the developer is migrating from HTTP to HTTPS, the following directive will ensure that all requests will be sent over HTTPS with no fallback to HTTP:

```text
Content-Security-Policy: upgrade-insecure-requests;
```

- To prevent all framing of your content use:
    - `Content-Security-Policy: frame-ancestors 'none';`
- To allow for the site itself, use:
    - `Content-Security-Policy: frame-an...
- [HTTP_Headers_Cheat_Sheet:003] HTTP Security Response Headers Cheat Sheet > Security Headers > X-Content-Type-Options: Use a Content Security Policy (CSP) that disables the use of inline JavaScript.

Do not set this header or explicitly turn it off.
> `X-XSS-Protection: 0`

Please see Mozilla X-XSS-Protection for details.

The `X-Content-Type-Options` response HTTP header is used by the server to indicate to the browsers that the MIME types advertised in the Content-Type headers should be followed and not guessed....
- [HTTP_Headers_Cheat_Sheet:025] HTTP Security Response Headers Cheat Sheet > Adding HTTP Headers in Different Technologies > Apache: The sample code below sets the `X-Frame-Options` header in PHP.

```php
header("X-Frame-Options: DENY");
```

Below is an `.htaccess` sample configuration which sets the `X-Frame-Options` header in Apache.

As described in the Apache documentation, `Header set` (default `onsuccess`) and `Header always set` operate on separate internal header tables.

In some cases, both header tables may be used, ...

## q26 (multi)
**Question:** My health app sends one-time codes by SMS: is SMS acceptable here, and should I hash the codes I store?
**Reference:** SMS should not protect apps holding PII such as health data (restricted authenticator); hashing OTPs is still recommended, for short-term exposure protection.
**Answer:** **Is SMS acceptable for a health app?**
No. NIST SP 800-63B-4 designates SMS and PSTN-delivered codes as a restricted authenticator due to SS7 interception, SIM-swap, and number-porting attacks [Multifactor_Authentication_Cheat_Sheet:028]. SMS should not be used to protect applications that hold Personally Identifiable Information (PII) or handle healthcare and banking [Multifactor_Authentication_Cheat_Sheet:028]. Where SMS is the only available factor, you must document risk acceptance, enforce per-account rate limits, monitor for SIM-swap signals, and plan a migration to TOTP, push notifications, or WebAuthn/FIDO2 [Multifactor_Authentication_Cheat_Sheet:028].

**Should you hash stored codes?**
Yes, you should not store OTPs in long-term plaintext form [Multifactor_Authentication_Cheat_Sheet:007]. While hashing OTPs does not provide strong offline brute-force resistance (due to their small keyspace, like ~1 million possibilities for a 6-digit code), hashing is still recommended to:
- Prevent accidental disclosure via logs, metrics, or debugging tools [Multifactor_Authentication_Cheat_Sheet:008]
- Reduce the blast radius if the database is briefly exposed during the OTP's validity window [Multifactor_Authentication_Cheat_Sheet:008]
- Enforce good secret-handling discipline and avoid plaintext storage by default [Multifactor_Authentication_Cheat_Sheet:008]
**Retrieved passages:**
- [Multifactor_Authentication_Cheat_Sheet:028] Multifactor Authentication Cheat Sheet > Something You Have > SMS Messages and Phone Calls: > [!WARNING]
> NIST SP 800-63B-4 designates SMS and PSTN-delivered codes as a *restricted* authenticator because of SS7 interception, SIM-swap, and number-porting attacks. Do not use SMS for high-value or PII-handling applications. Where it is the only available factor, document the risk acceptance, enforce per-account rate limits, monitor for SIM-swap signals, and plan migration to TOTP, push not...
- [Multifactor_Authentication_Cheat_Sheet:021] Multifactor Authentication Cheat Sheet > Something You Have > One-Time Password Tokens > Software OTP Tokens: A cheaper and easier alternative to hardware tokens is using software to generate Time-based One-Time Password (TOTP) codes. This would typically involve the user installing a TOTP application on their mobile phone, and then scanning a QR code provided by the web application which provides the initial seed. The authenticator app generates a numeric code using a configured time step; RFC 6238 recom...
- [Multifactor_Authentication_Cheat_Sheet:007] Multifactor Authentication Cheat Sheet > Implementing MFA > One-Time Password (OTP) Handling and Storage: OTPs are authentication secrets and should be handled with password-like hygiene. While their security traits differ from long-lived passwords, improper handling can still lead to user account compromise.

At a minimum, OTP implementations SHOULD:

- Enforce a short time-to-live (TTL)
- Ensure OTPs are single use
- Apply strict attempt limits
- Invalidate the OTP on successful verification

OTP im...
- [Multifactor_Authentication_Cheat_Sheet:029] Multifactor Authentication Cheat Sheet > Something You Have > SMS Messages and Phone Calls > Cons: - Relatively simple to implement.
- Requires user to link their account to a mobile number.

- Requires the user to have a mobile device or landline.
- Require user to have signal or internet access to receive the call or message.
- Calls and SMS messages may cost money to send need to protect against attackers requesting a large number of messages to exhaust funds.
- Susceptible to SIM swapping a...
- [Multifactor_Authentication_Cheat_Sheet:022] Multifactor Authentication Cheat Sheet > Something You Have > One-Time Password Tokens > Software OTP Tokens > Pros: - The absence of physical tokens greatly reduces the cost and administrative overhead of implementing the system.
- When users lose access to their TOTP app, a new one can be configured without needing to ship a physical token to them.
- TOTP is widely used, and many users will already have at least one TOTP app installed.
- A screen lock reduces theft risk but does not guarantee protection if the...
- [Multifactor_Authentication_Cheat_Sheet:008] Multifactor Authentication Cheat Sheet > Implementing MFA > One-Time Password (OTP) Handling and Storage > Hashing OTPs: Hashing OTPs is still recommended, but for different reasons than password hashing. OTPs typically have a very small keyspace (for example, ~1 million possibilities for a 6-digit code), which means a database attacker can brute-force any OTP hash quickly.

As a result, hashing OTPs does not provide strong offline attack resistance in the way password hashing does.

However, hashing remains useful ...
- [Multifactor_Authentication_Cheat_Sheet:009] Multifactor Authentication Cheat Sheet > Implementing MFA > One-Time Password (OTP) Handling and Storage > TOTP Seeds and Validation Window: The storage guidance above is for OTPs the server generates and sends. With TOTP the server instead keeps a long-lived shared seed and computes the expected codes from it, so the seed can't be hashed, and anyone who obtains it can generate valid codes until the user enrolls a new one. Strict attempt limits still apply to TOTP verification.

- Store TOTP seeds encrypted, ideally with a key held in ...
- [Forgot_Password_Cheat_Sheet:006] Forgot Password Cheat Sheet > Methods > General Security Practices: It is essential to employ good security practices for the reset identifiers (tokens, codes, PINs, etc.). Some points don't apply to the offline methods, such as the lifetime restriction. All tokens and codes should be:

- Generated using a cryptographically secure random number generator.
    - It is also possible to use JSON Web Tokens (JWTs) in place of random tokens, although this can introduce...

## q27 (multi)
**Question:** For a CV upload form, which file extensions should I allow and what file name should I store each file under?
**Reference:** Only business-critical extensions, e.g. docx and pdf for CVs; store each file under a random name such as a UUID.
**Answer:** For a CV upload, allow `docx` and `pdf` extensions [File_Upload_Cheat_Sheet:005]. 

Store each file under a random string generated by the application, such as a UUID/GUID [File_Upload_Cheat_Sheet:007, File_Upload_Cheat_Sheet:001].
**Retrieved passages:**
- [File_Upload_Cheat_Sheet:005] File Upload Cheat Sheet > File Upload Protection > Extension Validation > List Allowed Extensions: Ensure the usage of _business-critical_ extensions only, without allowing any type of _non-required_ extensions. For example if the system requires:

- image upload, allow one type that is agreed upon to fit the business requirement;
- cv upload, allow `docx` and `pdf` extensions.

Based on the needs of the application, ensure the **least harmful** and the **lowest risk** file types to be used....
- [File_Upload_Cheat_Sheet:007] File Upload Cheat Sheet > File Upload Protection > Filename Safety: In conjunction with content-type validation, validating the file's signature can be checked and verified against the expected file that should be received.

> This should not be used on its own, as bypassing it is pretty common and easy.

Filenames can endanger the system in multiple ways, either by using non acceptable characters, or by using special and restricted filenames. For Windows, refer t...
- [File_Upload_Cheat_Sheet:001] File Upload Cheat Sheet > Introduction: File upload is becoming a more and more essential part of any application, where the user is able to upload their photo, their CV, or a video showcasing a project they are working on. The application should be able to fend off bogus and malicious files in a way to keep the application and the users safe.

In short, the following principles should be followed to reach a secure file upload implement...
- [File_Upload_Cheat_Sheet:004] File Upload Cheat Sheet > File Upload Protection > Extension Validation: There is no silver bullet in validating user content. Implementing a defense in depth approach is key to make the upload process harder and more locked down to the needs and requirements for the service. Implementing multiple techniques is key and recommended, as no one technique is enough to secure the service.

Ensure that the validation occurs after decoding the filename, and that a proper filt...
- [File_Upload_Cheat_Sheet:006] File Upload Cheat Sheet > File Upload Protection > Content-Type Validation: Identify potentially harmful file types and block extensions that you regard harmful to your service.

Please be aware that blocking specific extensions is a weak protection method on its own. The Unrestricted File Upload vulnerability article describes how attackers may attempt
to bypass such a check.

_The Content-Type for uploaded files is provided by the user, and as such cannot be trusted, as...

## q28 (multi)
**Question:** When a user logs in, what should happen to their session ID, and how long must a hex-encoded session ID be?
**Reference:** Regenerate the session ID at login (any privilege change) and destroy the old one; at least 16 hexadecimal characters for 64 bits of entropy.
**Answer:** When a user logs in:
* The session ID must be renewed or regenerated by the web application to prevent session fixation attacks [Session_Management_Cheat_Sheet:030].
* Any previous session IDs must be ignored, the new session ID must be assigned to every new request for protected resources, and the old session ID must be destroyed [Session_Management_Cheat_Sheet:030].

For session ID length:
* When using hexadecimal encoding, a session ID must be **at least 16 hexadecimal characters** long to achieve the required 64 bits of entropy [Session_Management_Cheat_Sheet:006]. 
* If you create your own session ID, it is recommended to use a cryptographically secure pseudorandom number generator (CSPRNG) with a size of **at least 128 bits** [Session_Management_Cheat_Sheet:007].
**Retrieved passages:**
- [Session_Management_Cheat_Sheet:030] Session Management Cheat Sheet > Session ID Life Cycle > Renew the Session ID After Any Privilege Level Change: The session ID must be renewed or regenerated by the web application after any privilege level change within the associated user session. The most common scenario where the session ID regeneration is mandatory is during the authentication process, as the privilege level of the user changes from the unauthenticated (or anonymous) state to the authenticated state though in some cases still not yet t...
- [Session_Management_Cheat_Sheet:037] Session Management Cheat Sheet > Session Expiration > Automatic Session Expiration > Renewal Timeout: Alternatively, the web application can implement an additional renewal timeout after which the session ID is automatically renewed, in the middle of the user session, and independently of the session activity and, therefore, of the idle timeout.

After a specific amount of time since the session was initially created, the web application can regenerate a new ID for the user session and try to set ...
- [Session_Management_Cheat_Sheet:028] Session Management Cheat Sheet > Session ID Life Cycle > Session ID Generation and Verification: Permissive and Strict Session Management: There are two types of session management mechanisms for web applications, permissive and strict, related to session fixation vulnerabilities. The permissive mechanism allows the web application to initially accept any session ID value set by the user as valid, creating a new session for it, while the strict mechanism enforces that the web application will only accept session ID values that have b...
- [Session_Management_Cheat_Sheet:041] Session Management Cheat Sheet > Additional Client-Side Defenses for Session Management > Initial Login Timeout: Web applications can complement the previously described session management defenses with additional countermeasures on the client side. Client-side protections, typically in the form of JavaScript checks and verifications, are not bullet proof and can easily be defeated by a skilled attacker, but can introduce another layer of defense that has to be bypassed by intruders.

Web applications can us...
- [Session_Management_Cheat_Sheet:002] Session Management Cheat Sheet > Introduction: The session ID or token binds the user authentication credentials (in the form of a user session) to the user HTTP traffic and the appropriate access controls enforced by the web application. The complexity of these three components (authentication, session management, and access control) in modern web applications, plus the fact that its implementation and binding resides on the web developer's h...
- [Session_Management_Cheat_Sheet:006] Session Management Cheat Sheet > Session ID Properties > Session ID Length: As mentioned in the previous *Session ID Entropy* section, a primary security requirement for session IDs is that they contain at least `64 bits` of entropy to prevent brute-force guessing attacks. Although session ID length matters, it's the entropy that ensures security. The session ID must be long enough to encode sufficient entropy, preventing brute force attacks where an attacker guesses vali...
- [Session_Management_Cheat_Sheet:003] Session Management Cheat Sheet > Session ID Properties: In order to keep the authenticated state and track the users progress within the web application, applications provide users with a **session identifier** (session ID or token) that is assigned at session creation time, and is shared and exchanged by the user and the web application for the duration of the session (it is sent on every HTTP request). The session ID is a `name=value` pair.

With the...
- [Session_Management_Cheat_Sheet:005] Session Management Cheat Sheet > Session ID Properties > Session ID Entropy: Session identifiers must have at least `64 bits` of entropy to prevent brute-force session guessing attacks. Entropy refers to the amount of randomness or unpredictability in a value. Each “bit” of entropy doubles the number of possible outcomes, meaning a session ID with 64 bits of entropy can have `2^64` possible values.

A strong CSPRNG (Cryptographically Secure Pseudorandom Number Generator) m...
- [Session_Management_Cheat_Sheet:007] Session Management Cheat Sheet > Session ID Properties > Session ID Content (or Value): The session ID content (or value) must be meaningless to prevent information disclosure attacks, where an attacker is able to decode the contents of the ID and extract details of the user, the session, or the inner workings of the web application.

The session ID must simply be an identifier on the client side, and its value must never include sensitive information or Personally Identifiable Infor...
- [Session_Management_Cheat_Sheet:008] Session Management Cheat Sheet > Session Management Implementation: The session management implementation defines the exchange mechanism that will be used between the user and the web application to share and continuously exchange the session ID. There are multiple mechanisms available in HTTP to maintain session state within web applications, such as cookies (standard HTTP header), URL parameters (URL rewriting – RFC2396), URL arguments on GET requests, body argu...

## q29 (unanswerable)
**Question:** How do I implement PKCE in an OAuth 2.0 authorization code flow?
**Reference:** The corpus does not cover PKCE; check the OAuth 2.0 guidance.
**Answer:** The corpus does not cover this. The OWASP Cheat Sheets currently lack specific implementation details for PKCE in OAuth 2.0.
**Retrieved passages:**
- [Authentication_Cheat_Sheet:026] Authentication Cheat Sheet > Use of authentication protocols that require no password > OAuth 2.0 and 2.1: OAuth is an **authorization** framework for delegated access to APIs. See also: OAuth 2.0 Cheat Sheet.

> **Note:** OAuth 2.1 is an active IETF Working Group draft that consolidates OAuth 2.0 and widely adopted best practices and is intended to replace RFC 6749/6750; guidance in this cheat sheet applies to both OAuth 2.0 and OAuth 2.1. Because Internet-Drafts are revisioned, use the unversioned OA...
- [Authentication_Cheat_Sheet:027] Authentication Cheat Sheet > Use of authentication protocols that require no password > OpenID Connect (OIDC) > OIDC implementation guidance: **OpenID Connect 1.0 (OIDC)** is an identity layer **on top of OAuth**. It defines how a client (**relying party**) verifies the **end user's** identity using an **ID Token** (a signed JWT) and how to obtain user claims in an interoperable way. Use **OIDC for authentication/SSO**; use **OAuth for authorization** to APIs.

- **Validate ID Tokens** on the relying party: issuer (`iss`), audience (`au...
- [Session_Management_Cheat_Sheet:008] Session Management Cheat Sheet > Session Management Implementation: The session management implementation defines the exchange mechanism that will be used between the user and the web application to share and continuously exchange the session ID. There are multiple mechanisms available in HTTP to maintain session state within web applications, such as cookies (standard HTTP header), URL parameters (URL rewriting – RFC2396), URL arguments on GET requests, body argu...
- [Secrets_Management_Cheat_Sheet:016] Secrets Management Cheat Sheet > 2 General Secrets Management > 2.12 Passwordless Authentication and Token Security: OpenID Connect (OIDC) lets an application delegate user authentication to an identity provider (IdP), instead of storing and verifying the user's password itself. It does not require passwordless authentication: OpenID Connect Core Section 3.1.2.3 leaves the IdP's authentication method, including passwords, outside the protocol's scope.

OIDC alone does not eliminate phishing, credential stuffing,...
- [Forgot_Password_Cheat_Sheet:007] Forgot Password Cheat Sheet > Methods > URL Tokens: URL tokens are passed in the query string of the URL, and are typically sent to the user via email. The basic overview of the process is as follows:

1. Generate a token for the user and attach it in the URL query string.
2. Send this token to the user via email.
   - Don't rely on the Host header while creating the reset URLs to avoid Host Header Injection attacks. The URL should either be hard-c...
- [Authentication_Cheat_Sheet:001] Authentication Cheat Sheet > Introduction: **Authentication** (**AuthN**) is the process of verifying that an individual, entity, or website is who or what it claims to be by determining the validity of one or more authenticators (like passwords, fingerprints, or security tokens) that are used to back up this claim.

**Digital Identity** is the unique representation of a subject engaged in an online transaction. A digital identity is alway...

## q30 (unanswerable)
**Question:** Should I sign my JWTs with HS256 or RS256?
**Reference:** The corpus does not cover JWT signing algorithms.
**Answer:** The corpus does not cover this; the available cheat sheets mention JSON Web Tokens and signed ID tokens in OpenID Connect [Authentication_Cheat_Sheet:027], but do not provide guidance comparing HS256 and RS256 for signing JWTs.
**Retrieved passages:**
- [Cross-Site_Request_Forgery_Prevention_Cheat_Sheet:008] Cross-Site Request Forgery Prevention Cheat Sheet > Token-Based Mitigation > ALTERNATIVE: Using A Double-Submit Cookie Pattern > Signed Double-Submit Cookie (RECOMMENDED) > HMAC CSRF Token Generation and Validation: Compute HMAC-SHA-256 over an unambiguous encoding of the session-dependent value and random value described above, such as length-prefixed fields. Include the HMAC and random value in the token, and set the token cookie with the Secure attribute.

For each protected request, read the token from a submitted header or form field, never from the cookie alone. Reject requests with missing tokens or to...
- [Cross-Site_Request_Forgery_Prevention_Cheat_Sheet:006] Cross-Site Request Forgery Prevention Cheat Sheet > Token-Based Mitigation > ALTERNATIVE: Using A Double-Submit Cookie Pattern > Signed Double-Submit Cookie (RECOMMENDED): If maintaining the state for CSRF token on the server is problematic, you can use an alternative technique known as the Double Submit Cookie pattern. This technique is easy to implement and is stateless. There are different ways to implement this technique, where the _naive_ pattern is the most commonly used variation.

The most secure implementation of the Double Submit Cookie pattern is the _Sig...
- [Forgot_Password_Cheat_Sheet:006] Forgot Password Cheat Sheet > Methods > General Security Practices: It is essential to employ good security practices for the reset identifiers (tokens, codes, PINs, etc.). Some points don't apply to the offline methods, such as the lifetime restriction. All tokens and codes should be:

- Generated using a cryptographically secure random number generator.
    - It is also possible to use JSON Web Tokens (JWTs) in place of random tokens, although this can introduce...
- [Secrets_Management_Cheat_Sheet:039] Secrets Management Cheat Sheet > 7 Encryption > 7.1 Encryption Types to Use: Secrets Management goes hand in hand with encryption. After all, secrets must be stored encrypted somewhere to protect their confidentiality and integrity.

You can use various encryption types to secure a secret as long as they provide sufficient security, including adequate resistance against quantum computing-based attacks. Given that this is a moving field, it is best to follow current recomme...
- [Cross-Site_Request_Forgery_Prevention_Cheat_Sheet:007] Cross-Site Request Forgery Prevention Cheat Sheet > Token-Based Mitigation > ALTERNATIVE: Using A Double-Submit Cookie Pattern > Signed Double-Submit Cookie (RECOMMENDED) > Employing HMAC CSRF Tokens: To generate HMAC CSRF tokens (with a session-dependent user value), the system must have:

- **A session-dependent value that changes with each login session**. This value should only be valid for the entirety of the users authenticated session. Avoid using static values like the user's email or ID, as they are not secure (1 | 2 | 3). It's worth noting that updating the CSRF token too frequently, ...
- [Forgot_Password_Cheat_Sheet:007] Forgot Password Cheat Sheet > Methods > URL Tokens: URL tokens are passed in the query string of the URL, and are typically sent to the user via email. The basic overview of the process is as follows:

1. Generate a token for the user and attach it in the URL query string.
2. Send this token to the user via email.
   - Don't rely on the Host header while creating the reset URLs to avoid Host Header Injection attacks. The URL should either be hard-c...
- [Authentication_Cheat_Sheet:001] Authentication Cheat Sheet > Introduction: **Authentication** (**AuthN**) is the process of verifying that an individual, entity, or website is who or what it claims to be by determining the validity of one or more authenticators (like passwords, fingerprints, or security tokens) that are used to back up this claim.

**Digital Identity** is the unique representation of a subject engaged in an online transaction. A digital identity is alway...
- [Authentication_Cheat_Sheet:027] Authentication Cheat Sheet > Use of authentication protocols that require no password > OpenID Connect (OIDC) > OIDC implementation guidance: **OpenID Connect 1.0 (OIDC)** is an identity layer **on top of OAuth**. It defines how a client (**relying party**) verifies the **end user's** identity using an **ID Token** (a signed JWT) and how to obtain user claims in an interoperable way. Use **OIDC for authentication/SSO**; use **OAuth for authorization** to APIs.

- **Validate ID Tokens** on the relying party: issuer (`iss`), audience (`au...
- [Session_Management_Cheat_Sheet:007] Session Management Cheat Sheet > Session ID Properties > Session ID Content (or Value): The session ID content (or value) must be meaningless to prevent information disclosure attacks, where an attacker is able to decode the contents of the ID and extract details of the user, the session, or the inner workings of the web application.

The session ID must simply be an identifier on the client side, and its value must never include sensitive information or Personally Identifiable Infor...

## q31 (unanswerable)
**Question:** What query depth limit should I set on my GraphQL API?
**Reference:** The corpus does not cover GraphQL.
**Answer:** The corpus does not cover this. What is missing is specific guidance on the exact query depth limit value to set for a GraphQL API.
**Retrieved passages:**
- [Secrets_Management_Cheat_Sheet:031] Secrets Management Cheat Sheet > 4 Cloud Providers > 4.4 API limits: Cloud services can generally provide a limited amount of API calls over a given period. You could potentially (D)DoS yourself when you run into these limits. Most of these limits apply per account, project, or subscription, so spread workloads to limit your blast radius accordingly. Additionally, some services may support data key caching, preventing load on the key management service API (see, fo...
- [File_Upload_Cheat_Sheet:014] File Upload Cheat Sheet > File Upload Protection > Upload and Download Limits: The application should set proper size limits for the upload service in order to protect the file storage capacity. If the system is going to extract the files or process them, the file size limit should be considered after file decompression is conducted and by using secure methods to calculate zip files size. For more on this, see how to Safely extract files from ZipInputStream, Java's input str...
- [Input_Validation_Cheat_Sheet:004] Input Validation Cheat Sheet > Implementing Input Validation > Validate Structured Data: Use your framework's validators or a schema validator to enforce field rules. For JSON, explicitly configure required and additional properties; listing a property alone neither requires it nor rejects unknown fields. Apply schemas to nested objects and use item schemas and array length limits. Keep business checks, such as date ordering, alongside these structural checks.

Reject invalid requests...
- [Password_Storage_Cheat_Sheet:012] Password Storage Cheat Sheet > Password Hashing Algorithms > bcrypt > Input Limits of bcrypt: The bcrypt password hashing function **should only** be used for password storage in legacy systems where Argon2 and scrypt are not available.

The work factor should be as large as verification server performance will allow, with a minimum of 10.

bcrypt has a maximum length input length of 72 bytes for most implementations, so you should enforce a maximum password length of 72 bytes (or less if ...
- [Input_Validation_Cheat_Sheet:003] Input Validation Cheat Sheet > Implementing Input Validation > Parse Safely, Then Validate: Define what the application accepts and reject values outside those rules. Do not try to recognize every malicious string. Blocking apostrophes, for example, rejects legitimate names without making a database query safe. For free-form comments, an allowlist can permit broad Unicode text while limiting its length; it need not restrict users to letters and digits.

Apply request size limits before b...

## q32 (unanswerable)
**Question:** How do I protect my Node.js app against prototype pollution?
**Reference:** The corpus does not cover prototype pollution.
**Answer:** The corpus does not cover this. The OWASP Cheat Sheets currently do not contain guidance specifically addressing prototype pollution vulnerabilities in Node.js applications.
**Retrieved passages:**
- [Cross_Site_Scripting_Prevention_Cheat_Sheet:013] Cross Site Scripting Prevention Cheat Sheet > Safe Sinks: Security professionals often talk in terms of sources and sinks. If you pollute a river, it'll flow downstream somewhere. It’s the same with computer security. XSS sinks are places where variables are placed into your webpage.

Thankfully, many sinks where variables can be placed are safe. This is because these sinks treat the variable as text and will never execute it. Try to refactor your code t...
- [Cross-Site_Request_Forgery_Prevention_Cheat_Sheet:021] Cross-Site Request Forgery Prevention Cheat Sheet > Dealing with Client-Side CSRF Attacks (IMPORTANT): Client-side CSRF is a new variant of CSRF attacks where the attacker tricks the client-side JavaScript code to send a forged HTTP request to a vulnerable target site by manipulating the program's input parameters. Client-side CSRF originates when the JavaScript program uses attacker-controlled inputs, such as the URL, for the generation of asynchronous HTTP requests.

**Note:** These variants of C...
- [Cross-Site_Request_Forgery_Prevention_Cheat_Sheet:022] Cross-Site Request Forgery Prevention Cheat Sheet > Dealing with Client-Side CSRF Attacks (IMPORTANT) > Client-side CSRF Example: The following code snippet demonstrates a simple example of a client-side CSRF vulnerability.

```html
<script type="text/javascript">
    const csrf_token = document.querySelector("meta[name='csrf-token']").getAttribute("content");

    const ajaxLoad = () => {
        // process the URL hash fragment
        const hashFragment = window.location.hash.slice(1);

        // hash fragment should be ...
- [Cross_Site_Scripting_Prevention_Cheat_Sheet:007] Cross Site Scripting Prevention Cheat Sheet > Output Encoding > Output Encoding for “JavaScript Contexts”: When a server template inserts string data into an inline script, use an encoder documented for both the JavaScript string and the enclosing HTML script. The placeholder below represents data already encoded for that location; the template supplies the quotes:

```html
<script>const message = "ENCODED DATA";</script>
```

Do not insert untrusted code, identifiers, or expressions. Use a maintained ...
- [Server_Side_Request_Forgery_Prevention_Cheat_Sheet:002] Server-Side Request Forgery Prevention Cheat Sheet > Context: SSRF is an attack vector that abuses an application to interact with the internal/external network or the machine itself. One of the enablers for this vector is the mishandling of URLs, as showcased in the following examples:

- Image on an external server (*e.g.* user enters image URL of their avatar for the application to download and use).
- Custom WebHook (users have to specify Webhook handler...

## q33 (unanswerable)
**Question:** Which TLS version and cipher suites should my web server allow?
**Reference:** The corpus does not cover TLS versions or cipher suites.
**Answer:** The corpus does not cover this. The specific recommendations for allowed TLS versions and cipher suites are contained in the OWASP Transport Layer Security Cheat Sheet, which is referenced in the corpus [Session_Management_Cheat_Sheet:012] but whose contents are not indexed.
**Retrieved passages:**
- [Authentication_Cheat_Sheet:015] Authentication Cheat Sheet > Authentication General Guidelines > Consider Strong Transaction Authentication > TLS Client Authentication: Additionally, if the client is behind an enterprise proxy that performs SSL/TLS decryption, this will break certificate authentication unless the site is allowed on the proxy.

For more information, see: Client-authenticated TLS handshake...
- [HTTP_Headers_Cheat_Sheet:017] HTTP Security Response Headers Cheat Sheet > Security Headers > Server: Set it and disable all the features that your site does not need or allow them only to the authorized domains:
> `Permissions-Policy: geolocation=(), camera=(), microphone=()`

- *NOTE*: This example is disabling geolocation, camera, and microphone for all domains.

The `Server` header describes the software used by the origin server that handled the request — that is, the server that generated th...
- [Session_Management_Cheat_Sheet:013] Session Management Cheat Sheet > Session Management Implementation > Transport Layer Security: It is important to emphasize that TLS does not protect against session ID prediction, brute force, client-side tampering or fixation; however, it does provide effective protection against an attacker intercepting or stealing session IDs through a man in the middle attack....
- [Session_Management_Cheat_Sheet:012] Session Management Cheat Sheet > Session Management Implementation > Transport Layer Security: In order to protect the session ID exchange from active eavesdropping and passive disclosure in the network traffic, it is essential to use an encrypted HTTPS (TLS) connection for the entire web session, not only for the authentication process where the user credentials are exchanged. This may be mitigated by HTTP Strict Transport Security (HSTS) for a client that supports it.

Additionally, the `...
- [Content_Security_Policy_Cheat_Sheet:008] Content Security Policy Cheat Sheet > CSP Types (granular/allowlist based or strict): __DO NOT__ use `X-Content-Security-Policy` or `X-WebKit-CSP`. Their implementations are obsolete (since Firefox 23, Chrome 25), limited, inconsistent, and incredibly buggy.

For original research on allowlist weaknesses, see CSP Is Dead, Long Live CSP!.

The original mechanism for building a CSP involved creating allow-lists which would define the content and sources that were permitted in the con...
- [Authentication_Cheat_Sheet:009] Authentication Cheat Sheet > Authentication General Guidelines > Transmit Passwords Only Over TLS or Other Strong Transport: See: Transport Layer Security Cheat Sheet

The login page and all subsequent authenticated pages must be exclusively accessed over TLS or other strong transport. Failure to utilize TLS or other strong transport for the login page allows an attacker to modify the login form action, causing the user's credentials to be posted to an arbitrary location. Failure to utilize TLS or other strong transport...
- [Secrets_Management_Cheat_Sheet:049] Secrets Management Cheat Sheet > 10 Related Cheat Sheets & further reading: - CI/CD Security Cheat Sheet
- Key Management Cheat Sheet
- Logging Cheat Sheet
- Password Storage Cheat Sheet
- Cryptographic Storage Cheat Sheet
- OWASP WrongSecrets project...

## q34 (unanswerable)
**Question:** How many requests per minute should I allow per client on a public REST API?
**Reference:** The corpus does not give API rate-limit values.
**Answer:** The corpus does not cover this. The OWASP cheat sheets do not specify a concrete number of requests per minute to allow per client on a public REST API.
**Retrieved passages:**
- [Secrets_Management_Cheat_Sheet:031] Secrets Management Cheat Sheet > 4 Cloud Providers > 4.4 API limits: Cloud services can generally provide a limited amount of API calls over a given period. You could potentially (D)DoS yourself when you run into these limits. Most of these limits apply per account, project, or subscription, so spread workloads to limit your blast radius accordingly. Additionally, some services may support data key caching, preventing load on the key management service API (see, fo...
- [File_Upload_Cheat_Sheet:014] File Upload Cheat Sheet > File Upload Protection > Upload and Download Limits: The application should set proper size limits for the upload service in order to protect the file storage capacity. If the system is going to extract the files or process them, the file size limit should be considered after file decompression is conducted and by using secure methods to calculate zip files size. For more on this, see how to Safely extract files from ZipInputStream, Java's input str...
- [Secrets_Management_Cheat_Sheet:036] Secrets Management Cheat Sheet > 6 Implementation Guidance > 6.3 Ensure limitations are in place: Secrets should never be retrievable by everyone and everything. Always make sure that you put guardrails in place:

- Do you have the opportunity to create access policies? Ensure that there are policies in place to limit the number of entities that can read or write the secret. At the same time, write the policies so that you can easily extend them, and they are not too complicated to understand....
- [Authentication_Cheat_Sheet:022] Authentication Cheat Sheet > Authentication General Guidelines > Protect Against Automated Attacks > Login Throttling > Account Lockout: Login Throttling is a security mechanism used to prevent an attacker from making too many attempts at guessing a password through normal interactive means, it includes the following controls:

- Maximum number of attempts.

The most common protection against these attacks is to implement account lockout, which prevents any more login attempts for a period after a certain number of failed logins.

...
- [Forgot_Password_Cheat_Sheet:002] Forgot Password Cheat Sheet > Forgot Password Service > Forgot Password Request: The password reset process can be broken into two main steps, detailed in the following sections.

When a user uses the forgot password service and inputs their username or email, the below should be followed to implement a secure process:

- Return a consistent message for both existent and non-existent accounts.
- Ensure that responses return in a consistent amount of time to prevent an attacker...
