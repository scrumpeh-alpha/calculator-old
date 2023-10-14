import json

class SettingsJSONHandler():
    def __init__(self):
        with open('settings.json') as f:
            self.data = json.load(f)
            f.close()

    
    def getProperty(self, category: str, name: str):
        print(self.data['preferences']['colorscheme'])
        return self.data[category][name]
    
    def setProperty(self, category: str, name: str, value):
        with open('settings.json', 'w') as f:
            json.dump(
            {
                category: 
                {
                    name: value
                }
            }, 
            f, indent=4)
            f.close()

if __name__ == "__main__":
    jsonhandler= SettingsJSONHandler()
    jsonhandler.getProperty('preferences', 'colorscheme')
