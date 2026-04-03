tailwind.config = {
    theme:{
       extend:{
           gridTemplateColumns:{
            'auto': 'repeat(auto-fit, minmax(200px, 1fr))'
        },
        fontFamily:{
            Outfit: ["Manrope", "sans-serif"],
            Ovo: ["Sora", "sans-serif"]
        },
        animation:{
            spin_slow: 'spin 6s linear infinite'
        },
        colors:{
            lightHover: '#f4ede5',
            darkHover: '#1e293b',
            darkTheme: '#0f172a',
            accent: '#c46a3a',
            accentSoft: '#ead9cc',
            panel: '#fffaf5',
        },
        boxShadow:{
            'black': '4px 4px 0 #000',
            'white': '4px 4px 0 #fff',
        }
    }
},
      darkMode: 'selector'
}
