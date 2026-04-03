const sideMenu = document.querySelector('#sideMenu');
const menuOverlay = document.querySelector('#menuOverlay');
const menuToggleButton = document.querySelector('#menuToggleButton');
const navBar = document.querySelector("nav");
const navLinks = document.querySelector("nav ul");

function openMenu(){
    sideMenu.style.transform = 'translateX(-18rem)';
    menuOverlay?.classList.remove('hidden');
    document.body.classList.add('overflow-hidden');
    menuToggleButton?.setAttribute('aria-expanded', 'true');
}
function closeMenu(){
    sideMenu.style.transform = 'translateX(18rem)';
    menuOverlay?.classList.add('hidden');
    document.body.classList.remove('overflow-hidden');
    menuToggleButton?.setAttribute('aria-expanded', 'false');
}

window.addEventListener('scroll', ()=>{
    if(scrollY > 50){
       navBar.classList.add('bg-white', 'bg-opacity-50', 'backdrop-blur-lg', 'shadow-sm', 'dark:bg-darkTheme', 'dark:shadow-white/20');
       navLinks.classList.remove('bg-white', 'shadow-sm', 'bg-opacity-50', 'dark:border', 'dark:border-white/50', 'dark:hover:bg-transparent');

    }else{
        navBar.classList.remove('bg-white', 'bg-opacity-50', 'backdrop-blur-lg', 'shadow-sm', 'dark:bg-darkTheme', 'dark:shadow-white/20')
        navLinks.classList.remove('bg-white', 'shadow-sm', 'bg-opacity-50', 'dark:border', 'dark:border-white/50', 'dark:hover:bg-transparent');
    }
})

// ----------- light mode and dark mode ------------------

if (localStorage.theme === 'dark' || (!('theme in localStorage') && window. matchMedia('(prefers-color-scheme: dark)').matches)) {
    document.documentElement.classList.add('dark')
} else {
    document.documentElement.classList.remove('dark')
}

function toggleTheme(){
    document.documentElement.classList.toggle('dark');

    if(document.documentElement.classList.contains('dark')){
        localStorage.theme = 'dark';
    }else{
        localStorage.theme = 'light';
    }
}

const contactForm = document.querySelector('#contactForm');
const formStatus = document.querySelector('#formStatus');
const contactSubmitButton = document.querySelector('#contactSubmitButton');
const web3formsAccessKey = document.querySelector('#web3formsAccessKey');

if (contactForm && formStatus && contactSubmitButton && web3formsAccessKey) {
    const defaultButtonContent = contactSubmitButton.innerHTML;

    const setFormStatus = (message, isError = false) => {
        formStatus.textContent = message;
        formStatus.classList.remove(
            'hidden',
            'border-red-200',
            'bg-red-50',
            'text-red-700',
            'dark:border-red-400/30',
            'dark:bg-red-500/10',
            'dark:text-red-200',
            'border-emerald-200',
            'bg-emerald-50',
            'text-emerald-700',
            'dark:border-emerald-400/30',
            'dark:bg-emerald-500/10',
            'dark:text-emerald-200'
        );

        if (isError) {
            formStatus.classList.add(
                'border-red-200',
                'bg-red-50',
                'text-red-700',
                'dark:border-red-400/30',
                'dark:bg-red-500/10',
                'dark:text-red-200'
            );
        } else {
            formStatus.classList.add(
                'border-emerald-200',
                'bg-emerald-50',
                'text-emerald-700',
                'dark:border-emerald-400/30',
                'dark:bg-emerald-500/10',
                'dark:text-emerald-200'
            );
        }
    };

    contactForm.addEventListener('submit', async (event) => {
        event.preventDefault();

        const formData = new FormData(contactForm);
        const name = formData.get('name')?.toString().trim() || '';
        const email = formData.get('email')?.toString().trim() || '';
        const message = formData.get('message')?.toString().trim() || '';
        const accessKey = web3formsAccessKey.value.trim();
        const hasRealAccessKey = Boolean(accessKey);

        contactSubmitButton.disabled = true;
        contactSubmitButton.classList.add('opacity-70', 'cursor-not-allowed');
        contactSubmitButton.innerHTML = 'Sending...';
        formStatus.classList.add('hidden');

        try {
            if (hasRealAccessKey) {
                const response = await fetch(contactForm.action, {
                    method: 'POST',
                    body: formData
                });

                const result = await response.json();

                if (!response.ok || !result.success) {
                    throw new Error(result.message || 'Something went wrong while sending your message.');
                }

                contactForm.reset();
                setFormStatus('Thanks! Your message was sent successfully.');
            } else {
                const subject = encodeURIComponent(`Portfolio contact from ${name}`);
                const body = encodeURIComponent(
                    `Name: ${name}\nEmail: ${email}\n\nMessage:\n${message}`
                );

                window.location.href = `mailto:marympoyo1@gmail.com?subject=${subject}&body=${body}`;
                setFormStatus('Your email app is opening so you can send the message directly.');
            }
        } catch (error) {
            setFormStatus(error.message || 'The message could not be sent. Please try again.', true);
        } finally {
            contactSubmitButton.disabled = false;
            contactSubmitButton.classList.remove('opacity-70', 'cursor-not-allowed');
            contactSubmitButton.innerHTML = defaultButtonContent;
        }
    });
}

document.addEventListener('keydown', (event) => {
    if (event.key === 'Escape') {
        closeMenu();
    }
});

