# Model Management

Audapolis uses downloadable transcription models to convert speech to text. This guide explains how to download, manage, and choose the right models for your transcription needs.

## Understanding Transcription Models

### What Are Transcription Models?

**Speech Recognition Models**: Pre-trained AI models that convert spoken audio into written text. Each model is trained on specific languages and optimized for different use cases.

**Local Processing**: Models are downloaded and stored on your computer, ensuring transcription works offline and keeps your data private.

**Language-Specific**: Each model is designed for a specific language and won't work well with other languages.

### Model Types

**Small Models** (~40-50MB):
- **Pros**: Fast download, quick transcription, low memory usage
- **Cons**: Lower accuracy, struggles with technical terms
- **Best for**: Quick drafts, testing, resource-constrained systems
- **Speed**: 2-3x faster than big models

**Big Models** (~1-2GB):
- **Pros**: Higher accuracy, better with names and technical terms
- **Cons**: Larger download, slower transcription, more memory usage
- **Best for**: Final transcripts, professional work, accuracy-critical projects
- **Accuracy**: 10-20% more accurate than small models

## Accessing Model Management

### From Landing Page
1. Click the **gear icon** (⚙️) in the bottom-right corner
2. This opens the Model Manager showing all available languages

### From Menu Bar
1. Go to the main menu
2. Navigate to model management options

### Language-Specific Settings
1. In Model Manager, click on any language
2. Access detailed model options for that language

## Downloading Models

### Your First Model

**Required for Transcription**: You must download at least one transcription model before you can transcribe audio.

**Choosing Your First Model**:
1. Select your primary language (e.g., English, Spanish, French)
2. Start with a **small model** to test the workflow
3. Download a **big model** later for better accuracy

### Download Process

1. **Select Language**: Click on your desired language in the Model Manager
2. **Choose Model**: Click the download icon (☁️) next to your chosen model
3. **Monitor Progress**: Watch the download progress indicator
4. **Completion**: Model appears in "Downloaded" section when ready

### Download Requirements

**Internet Connection**: Required only for downloading models - transcription works offline afterward.

**Storage Space**: 
- Small models: 40-50MB each
- Big models: 1-2GB each
- Multiple languages require additional space

**Download Time**: Varies by connection speed and model size (few minutes for small models, 10-30 minutes for big models).

## Available Languages

### Fully Supported Languages

**Major Languages** (multiple model options):
- **English** (US/UK variants)
- **Spanish** 
- **French**
- **German**
- **Russian**
- **Chinese** (Mandarin)
- **Japanese**
- **Italian**
- **Dutch**
- **Portuguese/Brazilian Portuguese**

**Additional Languages** (single model options):
- **Arabic**
- **Hindi**
- **Korean**
- **Turkish**
- **Vietnamese**
- **Polish**
- **Czech**
- **Ukrainian**
- **Swedish**
- **Catalan**
- **Farsi (Persian)**
- **Filipino (Tagalog)**
- **Kazakh**
- **Esperanto**
- **Uzbek**
- **Breton**

### Language Variants

**English**: Separate models for US English and Indian English
**Chinese**: Multiple variants including specialized models
**Russian**: Multiple model sizes and variants
**French**: Standard and specialized models
**Dutch**: Multiple quality options

## Model Selection Strategy

### Choosing Between Model Sizes

**Start Small**:
1. Download a small model first
2. Test with representative audio samples
3. Evaluate if accuracy meets your needs
4. Upgrade to big model if necessary

**When to Use Small Models**:
- Quick transcription jobs
- Draft transcripts that will be heavily edited
- Limited storage or bandwidth
- Testing new languages

**When to Use Big Models**:
- Final, publication-ready transcripts
- Content with technical terms or proper names
- Professional or business use
- Maximum accuracy requirements

### Model Performance Factors

**Audio Quality Impact**: Both model types work better with clear, high-quality audio.

**Content Type Impact**:
- **Conversational**: Small models often sufficient
- **Technical/Professional**: Big models recommended
- **Names and Places**: Big models significantly better
- **Accents**: Big models more tolerant of variations

**Language Familiarity**: Languages with more training data (like English) generally perform better across all model sizes.

## Managing Downloaded Models

### Viewing Downloaded Models

**Model Manager**: Shows all downloaded models with details:
- Model name and size
- Language
- Download date
- Storage space used

**Default Model Selection**: For languages with multiple models, you can set which one to use by default.

### Setting Default Models

1. **Navigate to Language**: Click on a language with multiple downloaded models
2. **Select Default**: Choose which model to use for new transcriptions
3. **Radio Button**: Select the model you want as default
4. **Automatic Use**: New transcription projects will use this model automatically

### Deleting Models

**When to Delete**:
- Free up storage space
- Remove unused language models
- Replace small models after downloading big versions

**Deletion Process**:
1. Navigate to the language settings
2. Click the trash icon (🗑️) next to the model
3. Confirm deletion
4. Model is removed and storage space freed

**Note**: You cannot delete a model if it's the only one available for a language and you have projects using that language.

## Updating Models

### Model Updates

**Automatic Updates**: Currently, Audapolis doesn't automatically update models.

**Manual Updates**: 
1. Check for new Audapolis releases
2. New releases may include updated model lists
3. Download newer model versions if available
4. Remove older versions to save space

**Compatibility**: Newer model versions generally provide better accuracy and support for more languages.

## Storage Management

### Monitoring Storage Usage

**Total Space**: Model Manager shows total space used by all models.

**Per-Model Space**: Individual model sizes are displayed for each downloaded model.

**System Impact**: Models are stored in your system's application data directory.

### Storage Strategies

**Selective Downloads**: Only download models for languages you actively use.

**Size Management**: Balance between small and big models based on your needs.

**Regular Cleanup**: Periodically review and remove unused models.

**External Storage**: Models can be stored on external drives if needed (advanced users).

## Troubleshooting Model Issues

### Download Problems

**Slow Downloads**: 
- Check internet connection speed
- Try downloading during off-peak hours
- Pause other downloads or streaming

**Failed Downloads**:
- Restart Audapolis and try again
- Check available disk space
- Verify internet connectivity

**Corrupted Downloads**:
- Delete the failed model
- Clear application cache if needed
- Re-download the model

### Transcription Problems

**Poor Quality Results**:
- Try a bigger model for the same language
- Verify audio quality and language match
- Check that you selected the correct language

**Model Not Available**:
- Ensure you've downloaded a model for your language
- Check that download completed successfully
- Restart Audapolis if model doesn't appear

**Performance Issues**:
- Close other applications during transcription
- Try smaller models for faster processing
- Check available system memory

## Best Practices

### For New Users

1. **Start Simple**: Download one small model for your primary language
2. **Test First**: Try transcribing a short sample before committing to large downloads
3. **Evaluate Quality**: Determine if small model accuracy meets your needs
4. **Upgrade Strategically**: Download big models only for languages you use frequently

### For Professional Use

1. **Download Big Models**: Invest in accuracy for professional work
2. **Multiple Languages**: Download models for all languages you work with
3. **Default Settings**: Set appropriate default models for each language
4. **Regular Updates**: Check for new model releases periodically
5. **Storage Planning**: Plan adequate storage for multiple large models

### For Resource Management

1. **Monitor Usage**: Regularly check which models you actually use
2. **Clean Up**: Delete unused language models periodically
3. **Strategic Downloads**: Don't download "just in case" - download when needed
4. **Balance Quality**: Use small models for drafts, big models for final work

## Advanced Model Information

### Model Technology

**Based on Vosk**: Audapolis uses Vosk speech recognition models, which are based on Kaldi.

**Training Data**: Models are trained on large datasets of audio and text in each language.

**Continuous Improvement**: Model quality improves over time as training techniques advance.

### Performance Expectations

**Accuracy Ranges**:
- Small models: 85-95% accuracy on clear audio
- Big models: 90-98% accuracy on clear audio
- Actual accuracy depends heavily on audio quality and content type

**Speed Expectations**:
- Small models: Often faster than real-time
- Big models: Usually 2-5x slower than real-time
- Performance varies by system specifications

---

**Next**: Learn about [Settings & Preferences](settings-preferences.md) to customize Audapolis for your workflow.
