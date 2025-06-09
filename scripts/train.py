import argparse
from datasets import load_dataset
from transformers import AutoTokenizer, AutoModelForCausalLM, Trainer, TrainingArguments


def main():
    parser = argparse.ArgumentParser(description="Fine-tune a Korean language model")
    parser.add_argument('--model', type=str, default='skt/kogpt2-base-v2')
    parser.add_argument('--dataset', type=str, default='../data/legal_cases.jsonl')
    parser.add_argument('--output_dir', type=str, default='./model')
    args = parser.parse_args()

    dataset = load_dataset('json', data_files=args.dataset, split='train')
    tokenizer = AutoTokenizer.from_pretrained(args.model)
    model = AutoModelForCausalLM.from_pretrained(args.model)

    def tokenize_fn(example):
        return tokenizer(example['text'], truncation=True, padding='max_length', max_length=128)

    tokenized = dataset.map(tokenize_fn, batched=True)
    training_args = TrainingArguments(
        output_dir=args.output_dir,
        per_device_train_batch_size=2,
        num_train_epochs=1,
        logging_steps=1,
    )

    trainer = Trainer(model=model, args=training_args, train_dataset=tokenized)
    trainer.train()
    trainer.save_model(args.output_dir)


if __name__ == '__main__':
    main()
